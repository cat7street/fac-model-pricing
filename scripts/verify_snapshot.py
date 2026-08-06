#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "model_prices_and_context_window.json"
HASH_PATH = ROOT / "model_prices_and_context_window.sha256"
MODEL = "codex-auto-review"
EXPECTED = {
    "input_cost_per_token": 2e-7,
    "cache_read_input_token_cost": 2e-8,
    "output_cost_per_token": 1.2e-6,
}
FORBIDDEN_EXACT = {"batch", "flex", "cache_creation_input_token_cost"}
FORBIDDEN_PREFIXES = (
    "input_cost_per_token_",
    "output_cost_per_token_",
    "cache_read_input_token_cost_",
    "cache_creation_input_token_cost_",
    "long_context_",
)

body = DATA_PATH.read_bytes()
actual_hash = hashlib.sha256(body).hexdigest()
hash_fields = HASH_PATH.read_text(encoding="ascii").strip().split()
if len(hash_fields) != 2 or hash_fields[1] != DATA_PATH.name:
    raise SystemExit("invalid SHA-256 manifest format")
if hash_fields[0] != actual_hash:
    raise SystemExit(
        f"snapshot SHA-256 mismatch: manifest={hash_fields[0]} actual={actual_hash}"
    )

payload = json.loads(body)
entry = payload.get(MODEL)
if not isinstance(entry, dict):
    raise SystemExit(f"{MODEL} is missing or not an object")
for field, expected in EXPECTED.items():
    if entry.get(field) != expected:
        raise SystemExit(
            f"{MODEL}.{field}={entry.get(field)!r}; expected {expected!r}"
        )
if entry.get("cache_creation_input_token_cost", 0) != 0:
    raise SystemExit(f"{MODEL} cache-write price must be zero")

forbidden = sorted(
    key
    for key in entry
    if key in FORBIDDEN_EXACT or key.startswith(FORBIDDEN_PREFIXES)
)
if forbidden:
    raise SystemExit(f"{MODEL} contains unsupported pricing fields: {forbidden}")

print(
    json.dumps(
        {
            "models": len(payload),
            "sha256": actual_hash,
            "model": MODEL,
            "input": entry["input_cost_per_token"],
            "cache_read": entry["cache_read_input_token_cost"],
            "cache_write": 0,
            "output": entry["output_cost_per_token"],
        },
        sort_keys=True,
    )
)
