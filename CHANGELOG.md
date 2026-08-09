# Changelog

## 2.0.0 — Unreleased

### Data
- Added a pinned IANA registry snapshot and generated dataset workflow.
- Added temporary IANA 104.
- Updated current IANA names for 413 and 422.
- Marked IANA 418 unused and 510 obsoleted.
- Added vendor namespaces and collision-safe IDs.
- Added AWS ALB 464 and 562.
- Separated Cloudflare 530 from Pantheon 530.
- Added source quality and verification dates.

### CLI
- Added localized search.
- Added type, provider, and lifecycle filters.
- Fixed localized JSON export.
- Added strict language validation and collision-safe translation lookup.

### Web
- Added filters, provider-aware routes, translation coverage display, and read-only API endpoints.
- Added static permalink generation.
- Removed external font dependency and unsafe HTML string injection.
- Added security response headers.

### Quality
- Added offline validation, translation coverage reporting, dataset generation tests, modern CI, dependency automation, and scheduled live IANA drift checking.
