#!/usr/bin/env python3
"""Refresh the public Meetup member-count snapshot using Meetup's GraphQL API."""

import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://api.meetup.com/gql-ext"
NETWORK_URLNAME = "acm-local-network"
GROUP_URLNAME = "acm-austin"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "meetup-members.json"
QUERY = """
query($networkUrlname: ID!, $limit: Int!) {
  proNetwork(urlname: $networkUrlname) {
    groupsSearch(input: {first: $limit, filter: {}}) {
      edges {
        node {
          urlname
          memberships {
            totalCount
          }
        }
      }
    }
  }
}
"""


def fetch_member_count(token):
    body = json.dumps({
        "query": QUERY,
        "variables": {"networkUrlname": NETWORK_URLNAME, "limit": 100},
    }).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "acm-austin-member-count-sync",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise RuntimeError(f"Meetup API returned errors: {payload['errors']}")
    groups = (
        payload.get("data", {})
        .get("proNetwork", {})
        .get("groupsSearch", {})
        .get("edges", [])
    )
    for edge in groups:
        group = edge.get("node") or {}
        if group.get("urlname", "").lower() == GROUP_URLNAME:
            count = (group.get("memberships") or {}).get("totalCount")
            if isinstance(count, int) and count > 0:
                return count
            raise RuntimeError("Meetup API returned an invalid group member count")
    raise RuntimeError(f"Meetup group {GROUP_URLNAME!r} was not found in the network results")


def main():
    token = os.environ.get("MEETUP_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("Set the MEETUP_ACCESS_TOKEN environment variable")
    document = {
        "source": "Meetup API",
        "groupUrlname": GROUP_URLNAME,
        "memberCount": fetch_member_count(token),
        "updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    serialized = json.dumps(document, indent=2) + "\n"
    previous = OUTPUT.read_text() if OUTPUT.exists() else ""
    if previous == serialized:
        print("meetup-members.json already matches the Meetup API")
        return
    OUTPUT.write_text(serialized)
    print(f"Wrote {document['memberCount']:,} Meetup members to {OUTPUT}")


if __name__ == "__main__":
    main()