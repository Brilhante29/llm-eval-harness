# Technical Decision

- Runtime: Python 3.10+ CLI.
- Dependencies: standard library only.
- Input boundary: `contracts/prediction-artifact.schema.json`, version `1.0`.
- References: JSONL keyed by stable case ID.
- Predictions: one JSON artifact with producer project, version, run ID, timestamp, and case records.
- Validation: fail-fast on version, shape, duplicates, missing IDs, and unexpected IDs.
- Metrics: normalized exact match and token overlap F1.
- Output: shared portfolio benchmark contract with samples and string-valued environment metadata.
