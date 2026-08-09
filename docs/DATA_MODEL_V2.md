# HTTP Code Data Model v2

## Goals

The v2 model separates:

- IANA / RFC standard status codes
- Vendor-specific extensions (Cloudflare, Nginx, AWS, IIS, frameworks)
- Translation coverage
- Lifecycle state

## Example

```json
{
  "id": "standard-404",
  "code": 404,
  "type": "standard",
  "status": "active",
  "phrase": "Not Found",
  "source": {
    "name": "IANA",
    "url": "https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml"
  }
}
```

Vendor codes must have a provider namespace:

```json
{
  "id": "cloudflare-530",
  "code": 530,
  "type": "vendor",
  "provider": "cloudflare"
}
```

This avoids collisions where the same numeric code has different meanings across platforms.
