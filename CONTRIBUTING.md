# Contributing

Thanks for improving the HTTP status reference.

## Data changes

Do not edit `codes.json` by hand.

- Standards changes belong in `data/iana.json` and should match the IANA registry.
- Vendor changes belong in `data/vendors.json`.
- Every vendor entry needs a unique provider-prefixed `id`.
- Prefer vendor-owned documentation. If only community evidence exists, set `source.quality` accordingly and leave `verified_at` null until verified.
- Numeric codes may collide across providers; `(provider, code)` must stay unique.

After data changes run:

```bash
python tools/build_dataset.py
python tools/validate.py
python -m unittest discover -v
```

## Translation changes

Prefer v2 IDs (`iana-404`, `cloudflare-530`). Legacy numeric keys remain accepted only for standard IANA entries.

Do not describe a language as complete unless the coverage report confirms it.

## Web changes

Run:

```bash
npm run lint
npm run build
```

Avoid placing untrusted dataset strings into `innerHTML`; use DOM text nodes or `textContent`.
