# Security Policy

## Reporting a vulnerability

Please report security issues privately through GitHub's security reporting features when available rather than opening a public issue with exploit details.

Useful reports include the affected file or endpoint, reproduction steps, impact, and a suggested mitigation if known.

## Security posture

The web server is intentionally read-only. It disables the Express signature header and sends a restrictive Content Security Policy plus common browser hardening headers.

The Web UI treats status phrases, descriptions, translations, and provider names as data and inserts them through safe DOM text APIs rather than HTML injection.

Dependency and CI findings should be treated as maintenance signals; a dependency advisory does not automatically mean the application is exploitable.
