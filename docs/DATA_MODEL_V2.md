# Data model v2

`codes.json` is generated from two source files:

- `data/iana.json` — pinned snapshot of the IANA HTTP Status Code Registry.
- `data/vendors.json` — vendor-specific or ecosystem extensions.

Every entry has a globally unique `id`. Numeric status codes are **not** unique across vendors, so consumers must use `id` or the `(provider, code)` pair when they need an unambiguous identifier.

## Identity

Standard entries use IDs such as `iana-404`.
Vendor entries use provider-prefixed IDs such as `cloudflare-530`, `pantheon-530`, and `aws-alb-562`.

## Lifecycle

Allowed values are `active`, `temporary`, `unused`, and `obsoleted`.

## Source quality

`source.quality` is one of:

- `official` — standards registry or standards body.
- `vendor` — vendor-owned documentation.
- `community` — ecosystem evidence that still needs stronger verification.
- `historical` — preserved for compatibility/history and not treated as current authoritative behavior.

`verified_at` records the last date an authoritative source was checked. A null date is allowed for community/historical entries.

## Translations

v2 translation keys should use the unique entry ID:

```json
{
  "cloudflare-530": {
    "phrase": "...",
    "description": "..."
  }
}
```

Legacy numeric keys such as `"404"` remain supported **only for standard IANA entries**. This prevents a numeric translation from being incorrectly applied to two vendor meanings that share the same number.

## Generated data

Do not hand-edit `codes.json`. Edit `data/iana.json` or `data/vendors.json`, then run:

```bash
python tools/build_dataset.py
python tools/validate.py
```
