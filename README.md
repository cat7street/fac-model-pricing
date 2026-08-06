# FAC Model Pricing Snapshot

This public repository publishes immutable, audited model-pricing snapshots for FAC Sub2API production.

Production consumers must use raw URLs pinned to a full Git commit. Do not configure a branch URL such as `main` as a billing source.

The current snapshot is copied from FAC Sub2API commit `89fa2061219e1e778c4ab4755754e5c14c0ac200` and is verified by `scripts/verify_snapshot.py`.

## Contract

The verifier checks both the complete JSON SHA-256 and the dedicated `codex-auto-review` contract:

- input: `2e-7` USD per token
- cache read: `2e-8` USD per token
- cache write: `0` USD per token
- output: `1.2e-6` USD per token
- no inferred priority, batch, flex, or long-context pricing

## Verify

```sh
python3 scripts/verify_snapshot.py
```
