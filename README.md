<div align="center">

# HTTP Status Codes — Verified Reference

**IANA/RFC status codes + vendor-specific HTTP responses in one searchable, source-aware dataset.**

Cloudflare · AWS ALB · Nginx · Laravel · IIS · CLI · JSON · Web UI · Multilingual search

[![CI](https://github.com/MrAlfak/httpCode/actions/workflows/python-ci.yml/badge.svg)](https://github.com/MrAlfak/httpCode/actions/workflows/python-ci.yml)
[![Release](https://img.shields.io/github/v/release/MrAlfak/httpCode?display_name=tag&sort=semver)](https://github.com/MrAlfak/httpCode/releases/latest)
[![Stars](https://img.shields.io/github/stars/MrAlfak/httpCode?style=flat)](https://github.com/MrAlfak/httpCode/stargazers)
[![Forks](https://img.shields.io/github/forks/MrAlfak/httpCode?style=flat)](https://github.com/MrAlfak/httpCode/forks)
[![License](https://img.shields.io/github/license/MrAlfak/httpCode)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-informational)](pyproject.toml)
[![Node](https://img.shields.io/badge/Node-18%2B-informational)](package.json)

**[Quick start](#quick-start) · [CLI](#cli) · [Web API](#web-api) · [Data model](docs/DATA_MODEL_V2.md) · [Contribute](CONTRIBUTING.md) · [Roadmap](ROADMAP.md)**

</div>

---

## Why this exists

Most HTTP status-code lists treat a number as if it has one universal meaning. Real systems are messier.

`530`, for example, can mean different things depending on the platform. **httpCode keeps standard IANA statuses and vendor-specific responses separate, source-aware, and collision-safe.**

Use it when you are building APIs, debugging production incidents, writing documentation, teaching HTTP, creating monitoring tools, validating status-code datasets, or simply need a reliable answer fast.

> ⭐ If httpCode saves you time, consider starring the repository. It helps more developers discover it.

## What makes httpCode different?

| Capability | httpCode |
|---|---|
| IANA / RFC status codes | ✅ |
| Vendor-specific codes | ✅ |
| Collision-safe provider namespaces | ✅ |
| Lifecycle state (`active`, `temporary`, `unused`, `obsoleted`) | ✅ |
| Source + verification metadata | ✅ |
| Cloudflare / AWS ALB / Nginx / Laravel / IIS coverage | ✅ |
| Searchable Web UI | ✅ |
| Python CLI | ✅ |
| JSON / CSV / Markdown export | ✅ |
| Multilingual search and translations | ✅ |
| Read-only Web API | ✅ |
| JSON Schema + offline validation | ✅ |
| Scheduled IANA drift checks | ✅ |

## Quick start

### Search from the CLI

```bash
git clone https://github.com/MrAlfak/httpCode.git
cd httpCode

python httpcode.py 404
python httpcode.py timeout
python httpcode.py all --type vendor --provider cloudflare
python httpcode.py all --status obsoleted
```

Search translated content too:

```bash
python httpcode.py "پیدا نشد" --lang fa
python httpcode.py 4xx --lang fa --export json --out errors-fa.json
```

### Run the Web UI

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

The explorer supports keyword search plus filters for **type, provider, lifecycle, and language**.

## Useful examples

```text
404
4xx
timeout
cloudflare
aws
nginx
temporary
obsoleted
```

Provider-aware URLs prevent collisions:

```text
/status/404
/status/cloudflare/530
/status/pantheon/530
```

## Web API

The local server exposes a small read-only API:

```text
GET /api/codes
GET /api/codes?type=vendor&provider=cloudflare
GET /api/codes?status=obsoleted
GET /api/status/404
GET /api/status/cloudflare/530
GET /api/languages
```

Example:

```bash
curl "http://localhost:3000/api/codes?type=vendor&provider=cloudflare"
```

## Data you can trust and inspect

Standard entries are pinned to the IANA HTTP Status Code Registry and keep lifecycle information explicit.

Examples of details modeled by v2:

- IANA `104` is tracked as temporary.
- Current IANA names such as `413 Content Too Large` and `422 Unprocessable Content` are used.
- IANA `418` is represented as `(Unused)`.
- `510 Not Extended` is marked obsoleted.
- Vendor entries use unique IDs such as `cloudflare-530`.
- Cloudflare `530` and Pantheon `530` coexist without overwriting one another.
- AWS Application Load Balancer `464` and `562` are included.
- Source quality and verification dates are retained.

## Project layout

```text
codes.json             Generated compatibility dataset
data/iana.json         Pinned IANA registry snapshot
data/vendors.json      Vendor-specific extensions
i18n/                  Translation data
schema/                 JSON Schema
tools/build_dataset.py Dataset generator
tools/validate.py      Offline validation
tools/check_iana.py    Live IANA drift check
tools/i18n_coverage.py Translation coverage report
web/                   Searchable web explorer
```

See [`docs/DATA_MODEL_V2.md`](docs/DATA_MODEL_V2.md) for the schema and data-model rules.

## Internationalization

Translation files can be partial; coverage is measured instead of guessed.

```bash
python tools/i18n_coverage.py
```

Legacy numeric translation keys such as `"404"` still work for standard entries. New vendor translations should use unique IDs such as `"cloudflare-530"`.

## Validation and maintenance

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

The normal validator works offline. The live IANA drift check requires network access and also runs on a schedule in GitHub Actions.

## Who is this for?

- Backend and API developers
- Frontend developers handling API errors
- DevOps / SRE / platform teams
- Technical writers and API documentation teams
- Security and observability tooling
- Students and educators learning HTTP
- SDK, framework, proxy, CDN, and gateway authors

## Contributing

Contributions are welcome — especially:

- verified vendor-specific status codes
- corrections with primary sources
- translation improvements
- accessibility and Web UI improvements
- tests and tooling
- documentation and examples

Start with [`CONTRIBUTING.md`](CONTRIBUTING.md), or open a structured issue using the repository templates.

Please read the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) before participating.

## Roadmap

See [`ROADMAP.md`](ROADMAP.md) for planned improvements and good first contribution areas.

## Support

See [`SUPPORT.md`](SUPPORT.md) for the fastest way to ask for help or report a data problem.

## Cite this project

A [`CITATION.cff`](CITATION.cff) file is included so GitHub and citation tools can generate citation metadata automatically.

## Security

See [`SECURITY.md`](SECURITY.md).

## License

MIT — see [`LICENSE`](LICENSE).

---

<div align="center">

Built as an open, inspectable HTTP reference for developers.

**Useful? ⭐ Star it · Fork it · Improve it**

</div>
