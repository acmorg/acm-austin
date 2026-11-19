# ACM Austin Website

The public-facing website for the Austin ACM / IEEE engineering community. It is currently a responsive single-page site built from one static HTML file.

Everyone is welcome to help improve it. You do not need to be an ACM member or a frontend expert to contribute: report a typo, suggest a better event detail, improve accessibility, add an approved photo, or open a small pull request.

Repository: https://github.com/acmorg/acm-austin

Live site: `https://acmorg.github.io/acm-austin/` after GitHub Pages is enabled.

## Quick Start

No build step is required.

```bash
open index.html
```

For a local HTTP server, use any static server, for example:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Deploy With GitHub Pages

The repository includes a GitHub Actions workflow at `.github/workflows/pages.yml`. It publishes the repository root whenever `main` receives a push.

One-time repository setup:

1. Open the repository's **Settings** on GitHub.
2. Select **Pages** under **Code and automation**.
3. Set **Source** to **GitHub Actions**.
4. Push to `main` and open the URL shown in the workflow's deployment summary.

The workflow publishes the static site as-is, including `index.html`, `sessionize.html`, and `photos/`.

Typical update flow:

```bash
git status
git add .
git commit -m "Describe the change"
git push origin main
```

## Project Structure

- `index.html` - page markup, Tailwind CDN configuration, event rendering, countdown, and form behavior.
- `sessionize.html` - live Sessionize sessions and speaker directory sub-page.
- `photos/` - local speaker, volunteer, and community photography.
- `TODO.md` - implementation plan for Sessionize, Meetup, and Luma integrations.
- `CONTRIBUTING.md` - contribution and review guidelines.

## Current Integrations

The page links to the chapter's Meetup, LinkedIn, Sessionize, and venue map pages. The JavaScript includes API-ready adapters named `fetchMeetupEvents`, `fetchLumaEvents`, and `fetchSessionizeData`. Meetup API credentials must be handled server-side rather than committed to the browser.

The Meetup member count is displayed from `meetup-members.json`. The scheduled `.github/workflows/sync-meetup-members.yml` workflow refreshes it weekly using Meetup GraphQL and deploys the updated static site. Add a valid `MEETUP_ACCESS_TOKEN` secret to the `github-pages` GitHub Actions environment to enable automatic API updates. The checked-in starting count, 2,117, was verified against the public Meetup group page on November 19, 2026.

## Volunteer Form Storage

The volunteer section embeds the Google Form connected to the chapter's response spreadsheet. The edit URL must remain private; the page uses the public `viewform` URL. Review the form's sharing settings, response access, retention, and spam protection before collecting real attendee data.

Public forms:

- [Volunteer signup form](https://docs.google.com/forms/d/1f_ucupsckbus_6K4Qd5OI2gOVTxNdLt0rQpzXUctnxI/viewform)
- [Sponsorship interest form](https://docs.google.com/forms/d/e/1FAIpQLSc8HPaboM9NUODwUT-upXe4gyXFqnrG_s37TalQi6HpJ4n2_A/viewform?usp=dialog)

## Contributing

Have an idea or found something that could be better? [Open an issue](https://github.com/acmorg/acm-austin/issues) with a clear description, screenshots when useful, and steps to reproduce a problem. For changes you can implement, fork the repository, create a focused branch, and [open a pull request](https://github.com/acmorg/acm-austin/pulls).

Good contributions include:

- Improving mobile layout, keyboard navigation, or alt text.
- Correcting event, venue, speaker, or sponsor information.
- Adding optimized, approved community photography.
- Improving documentation or the integration TODOs.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting. Keep pull requests focused, explain how you tested them, and never commit API keys, private form links, personal attendee data, or unapproved media.

## Adding Photos

Place optimized images in `photos/` and reference them with relative paths such as `photos/speaker-name.webp`. Prefer WebP or compressed JPEG files, descriptive filenames, and meaningful `alt` text. Do not commit private or unapproved images.

## Content Updates

Update the `EVENTS` array in `index.html` until the API adapters are connected. Keep event dates in ISO 8601 format with the correct Austin offset. Verify event links, venue details, accessibility copy, and mobile layout before publishing.

## Credits

Starter project by Prachi Jethava (`@prachi1211`).

Contributors:

- Akshay Mittal (`@akshaymittal143`)
- Prachi Jethava (`@prachi1211`)
