# Integration Plan

This checklist tracks the path from local placeholder data to reliable event and community operations.

## Foundation

- [ ] Decide which source is authoritative for event title, date, venue, description, RSVP URL, and attendance count.
- [ ] Create a small server-side API proxy or serverless function; keep all provider tokens out of `index.html`.
- [ ] Define one normalized event schema shared by Meetup and Luma adapters.
- [ ] Add environment variables for provider credentials, organizer IDs, and cache duration.
- [ ] Add loading, empty, stale-data, and provider-error states to the event grid.

## Sessionize: speaker pipeline

- [ ] Confirm the Sessionize event or organization endpoint and available public fields.
- [ ] Decide whether accepted sessions should be public before an event is published.
- [ ] Add a server-side `GET /api/sessionize` adapter with response validation.
- [ ] Render accepted speakers or open submission status from normalized data.
- [ ] Keep the direct Sessionize submission CTA available if the API is unavailable.
- [ ] Add caching and a fallback message for rate limits or downtime.

## Meetup: event and RSVP pipeline

- [ ] Create or confirm a Meetup OAuth app and organizer permissions.
- [ ] Store the Meetup client secret server-side and implement OAuth/token refresh.
- [ ] Add `GET /api/meetup-events` with pagination and a future-date filter.
- [ ] Normalize Meetup locations, images, RSVP URLs, and attendance counts.
- [ ] Replace the local `EVENTS` fallback only after the adapter passes fixture tests.
- [ ] Verify rate limits, timezone handling, cancellations, and sold-out states.

Recommended rollout: keep the static GitHub Pages site as the frontend, add a small serverless API proxy for Meetup, and publish only normalized public event data to the browser. Start with read-only upcoming events and RSVP links; add organizer actions or attendee data only after permissions, consent, and data retention are confirmed.

## Luma: alternative event source

- [ ] Confirm whether Luma is a source of record or a secondary calendar.
- [ ] Obtain API access and document the event collection ID and permissions.
- [ ] Add `GET /api/luma-events` with pagination and response validation.
- [ ] Normalize Luma fields to the shared event schema and deduplicate by canonical URL.
- [ ] Define conflict rules when Meetup and Luma describe the same event differently.
- [ ] Add provider attribution only where it helps attendees understand the RSVP path.

## Certifier: speaker and volunteer certificates

POC: Akshay Mittal

Dashboard: https://app.certifier.io/dashboard

- [ ] Confirm Certifier workspace access, API availability, and the certificate templates for speakers and volunteers.
- [ ] Decide the award rules: speaker session delivered, volunteer shift completed, or organizer approval.
- [ ] Define the certificate data fields, including recipient name, role, event title, event date, issuer, and verification URL.
- [ ] Store Certifier credentials server-side and add a protected certificate issuance endpoint.
- [ ] Connect approved speaker and volunteer records to Certifier issuance requests.
- [ ] Add an idempotency key so retries cannot issue duplicate certificates.
- [ ] Save certificate IDs and verification URLs against the event participation record.
- [ ] Add a private organizer view for reviewing, reissuing, or revoking certificates.
- [ ] Obtain recipient consent before collecting names and email addresses for certificates.
- [ ] Test a complete proof of concept with Akshay before enabling automatic issuance.

## Launch and operations

- [ ] Add automated tests for normalization, countdown dates, duplicate events, and malformed provider responses.
- [ ] Add an integration health check or lightweight admin status page.
- [x] Embed the Google Form public `viewform` URL for volunteer submissions.
- [ ] Confirm the Google Form response spreadsheet permissions and organizer notification settings.
- [ ] Add a custom confirmation message and response retention policy in Google Forms.
- [ ] Alternative if the organizers want spreadsheet ownership: use a Google Apps Script web app that validates the fields and appends rows to a restricted Google Sheet.
- [ ] Add consent, retention, and spam protection before collecting submissions in production.
- [ ] Add a scheduled refresh job and monitor failed syncs.
- [ ] Document the final deployment command, environment variables, and rollback process.
