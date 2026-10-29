# Contributing

Keep FEX's router small and specialist-oriented. Do not copy third-party skill content into FEX; update `plugins/fex/upstream.lock.json` to change an upstream version and document why.

Before a pull request:

```bash
python3 tests/test_bundle.py
python3 scripts/validate.py
```

When changing routing behavior, add or update an eval case under `tests/router_cases.md`. When changing an upstream pin, verify the new commit and review its license before merging.
