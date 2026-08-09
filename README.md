# HTTP Status Codes (Standard & Unofficial)

A developer reference for HTTP status codes with separated standard (IANA/RFC) and vendor-specific meanings.

## v2 improvements

- Standard and vendor codes are modeled separately.
- Vendor collisions (for example Cloudflare/Nginx/AWS codes) are handled with provider namespaces.
- Dataset validation schema is available in `schema/http-code.schema.json`.
- Translation coverage is tracked instead of assuming every language has full coverage.

## Features

- Standard HTTP status reference.
- Unofficial platform codes.
- CLI search and export.
- Web explorer.
- Multi-language support.
- Developer-friendly JSON datasets.

## Development

Run the web server instead of opening HTML directly:

```bash
node server.js
```

Then open the local server URL.

## Data quality rules

New status entries should include:

- Source authority (IANA, RFC, vendor documentation)
- Lifecycle state
- Provider namespace for vendor codes
- Translation coverage status

## License

MIT License.
