# Contributing

Thanks for helping ACM Austin make useful engineering events easier to find.

## Before You Start

1. Create a focused branch for your change.
2. Check `TODO.md` and avoid duplicating work already in progress.
3. For content or photography, confirm that ACM Austin has permission to publish it.
4. For a substantial change, open an issue first so scope and ownership are clear.

## Good First Contributions

Useful contributions include correcting event details, improving keyboard navigation, adding alt text, optimizing approved photos, improving mobile layout, and documenting integration work. Please do not add invented event data, unapproved personal information, or credentials.

## Local Review

Open the page directly with `open index.html`, or run:

```bash
python3 -m http.server 8000
```

Before opening a pull request, check:

- The page works at desktop and mobile widths.
- Navigation, external links, countdown, event cards, and the volunteer form behave correctly.
- New images have useful `alt` text and are optimized.
- No API keys, tokens, personal data, or generated build artifacts are committed.
- `get_errors` or an equivalent HTML/JavaScript check reports no new errors.

## Code Style

Keep the site dependency-light and preserve the existing Tailwind CDN approach until a build system is intentionally introduced. Keep event data normalized, use semantic HTML, and prefer accessible labels, focus states, and keyboard-friendly controls.

## Pull Requests

Describe what changed, how it was tested, and whether the change affects event data, external integrations, accessibility, or privacy. Keep unrelated formatting and content changes out of the same pull request.

Prefer small, reviewable pull requests with a clear title and screenshots for visual changes. Link the related issue, call out any follow-up work, and confirm that external links and mobile states were checked. Maintainers may request changes when content ownership, accessibility, privacy, or security is unclear.

## Review Standards

Reviewers look for correctness, accessibility, responsive behavior, clear ownership of content and images, and protection of secrets and personal data. Discussion should stay specific and respectful. See `CODE_OF_CONDUCT.md` for community expectations.
