# Local Setup

## Quickstart (Online)
1. Run `make setup`.
2. Run `make test`.
3. Run `make demo-a`.

## Quickstart (Offline)
1. While online once, run `make setup` then `make vendor`.
2. Disconnect from internet.
3. Run `make setup-offline`.
4. Run `make test` and demos (`make demo-a`, `make demo-b`, `make demo-c`).

## Wheelhouse Notes
- Default wheelhouse path: `.vendor/wheels`.
- You can override with: `make setup-offline WHEELHOUSE_DIR=/path/to/wheels`.
- The wheelhouse directory is gitignored by default to avoid repository bloat.

## Runtime Offline Guarantee
- `OFFLINE_MODE=true` keeps demo runs local and fixture-only.
- Demos process files under `fixtures/`; they do not fetch internet content.
