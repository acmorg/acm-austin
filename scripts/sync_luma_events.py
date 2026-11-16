#!/usr/bin/env python3
"""Refresh events.json from the public ACM Austin Luma calendar."""

import json
import urllib.request
from pathlib import Path

CALENDAR_ID = "cal-HidBA3hMcIwKB1L"
API_URL = "https://api.lu.ma/calendar/get-items"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "events.json"


def fetch_entries():
    entries = []
    cursor = None
    while True:
        url = f"{API_URL}?calendar_api_id={CALENDAR_ID}&period=future"
        if cursor:
            url += f"&pagination_cursor={urllib.request.quote(cursor)}"
        request = urllib.request.Request(
            url,
            headers={"Accept": "application/json", "User-Agent": "acm-austin-event-sync"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
        entries.extend(payload.get("entries") or [])
        cursor = payload.get("next_cursor")
        if not payload.get("has_more") or not cursor:
            return entries


def normalize(entry):
    event = entry.get("event") or {}
    if not event.get("start_at") or not event.get("api_id"):
        return None
    if event.get("visibility") not in (None, "public"):
        return None
    address = event.get("geo_address_info") or {}
    venue = address.get("address") or "Austin"
    short = address.get("short_address") or address.get("city_state") or ""
    tags = [tag.get("name") for tag in (entry.get("tags") or []) if tag.get("name")]
    event_type = "Workshop" if any("workshop" in tag.lower() for tag in tags) else "Tech talks"
    return {
        "date": event["start_at"],
        "end": event.get("end_at"),
        "timezone": event.get("timezone") or "America/Chicago",
        "type": event_type,
        "title": event.get("name") or "ACM Austin event",
        "description": f"{venue}, {short}" if short else venue,
        "tags": tags[:4],
        "going": entry.get("guest_count") or 0,
        "lumaEventId": event["api_id"],
        "url": f"https://luma.com/event/{event['api_id']}",
    }


def main():
    events = [item for item in (normalize(entry) for entry in fetch_entries()) if item]
    events.sort(key=lambda item: item["date"])
    document = {"source": "luma", "calendarId": CALENDAR_ID, "events": events}
    serialized = json.dumps(document, indent=2) + "\n"
    previous = OUTPUT.read_text() if OUTPUT.exists() else ""
    if previous == serialized:
        print("events.json already matches the Luma calendar")
        return
    OUTPUT.write_text(serialized)
    print(f"Wrote {len(events)} upcoming event(s) to {OUTPUT}")


if __name__ == "__main__":
    main()
