## What changed?

Describe the change and the developer/user impact.

## Why?

Explain the problem this solves.

## Data source (if applicable)

For status-code data changes, link the primary IANA/RFC/vendor source and identify the provider + code.

## Validation

- [ ] `python tools/build_dataset.py`
- [ ] `python tools/validate.py`
- [ ] `python -m unittest discover -v`
- [ ] `npm run lint`
- [ ] `npm run build`
- [ ] Documentation updated when behavior changed

## Checklist

- [ ] I did not edit generated `codes.json` manually.
- [ ] Vendor entries use a collision-safe provider-prefixed ID.
- [ ] User-controlled strings are not injected through unsafe HTML.
- [ ] The change is focused and does not include unrelated edits.
