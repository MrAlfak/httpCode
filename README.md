# HTTP Status Codes — Verified Reference

A developer-focused reference for **standard IANA HTTP status codes** and **vendor-specific HTTP responses** from platforms such as Cloudflare, AWS Application Load Balancer, Nginx, Laravel, IIS, and others.

The project intentionally does **not** assume that a numeric code has only one meaning. For example, vendor-specific `530` responses are namespaced separately.

## What changed in v2

- Standard statuses are pinned to the IANA HTTP Status Code Registry.
- Lifecycle states are explicit: `active`, `temporary`, `unused`, `obsoleted`.
- Vendor responses use globally unique IDs such as `cloudflare-530`.
- Cloudflare `530` and Pantheon `530` can coexist without overwriting each other.
- AWS ALB `464` and `562` are included.
- IANA `104` is tracked as temporary.
- Current IANA names such as `413 Content Too Large` and `422 Unprocessable Content` are used.
- `418` is represented as IANA `(Unused)` instead of being presented as a current standard reason phrase.
- `510` is marked obsoleted.
- Translation coverage is measured instead of claiming every language is complete.
- Search works against localized text.
- JSON export now exports localized text too.
- The Web UI uses safe DOM APIs instead of injecting dataset strings through `innerHTML`.
- Static permalinks and a small read-only API are available.
- Dataset validation and scheduled IANA drift checks are included.

## Data layout

```text
codes.json             Generated compatibility dataset
data/iana.json         Pinned IANA registry snapshot
data/vendors.json      Vendor-specific extensions
schema/                 JSON Schema
tools/build_dataset.py Dataset generator
tools/validate.py      Offline validation
tools/check_iana.py    Live IANA drift check
tools/i18n_coverage.py Translation coverage report
```

See [`docs/DATA_MODEL_V2.md`](docs/DATA_MODEL_V2.md) for the data model.

## Run the Web UI

Do **not** open `web/index.html` directly with `file://`.

```bash
npm install
npm run dev
```

Then open `http://localhost:3000`.

## Web API

```text
GET /api/codes
GET /api/codes?type=vendor&provider=cloudflare
GET /api/status/404
GET /api/status/cloudflare/530
GET /api/languages
```

The API is intentionally read-only.

## CLI

```bash
python httpcode.py 404
python httpcode.py "پیدا نشد" --lang fa
python httpcode.py all --type vendor --provider cloudflare
python httpcode.py all --status obsoleted
python httpcode.py 4xx --lang fa --export json --out errors-fa.json
python httpcode.py --list-langs
```

## Translation coverage

Translation files may be partial. Measure them explicitly:

```bash
python tools/i18n_coverage.py
```

Legacy numeric translation keys (`"404"`) still work for standard entries. New vendor translations should use globally unique IDs such as `"cloudflare-530"`.

## Data maintenance

After editing source data:

```bash
python tools/build_dataset.py
python tools/validate.py
python -m unittest discover -v
npm run lint
npm run build
```

To compare the pinned standards snapshot with the live IANA registry:

```bash
python tools/check_iana.py
```

The live check requires network access. The normal validator is fully offline.

## Source policy

Preferred source order:

1. IANA / RFC / IETF
2. Vendor-owned documentation
3. Community evidence when an official source is unavailable
4. Historical entries only when useful for compatibility

Entries with weaker sources are intentionally marked with `source.quality` and may have `verified_at: null`.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Changes to status data should include a source and must pass validation.

## Security

See [`SECURITY.md`](SECURITY.md).

## License

MIT.
