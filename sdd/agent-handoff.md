# Agent Handoff

Project: `2 - llm-eval-harness`

## Current State

- References and predictions are separate artifacts.
- `prediction-artifact/1.0` is documented and versioned under `contracts/`.
- The committed producer fixture identifies `rag-knowledge-base` and can be replaced by any conforming producer output.
- Duplicate, missing, unexpected, and version-invalid inputs have tests.
- Output satisfies the shared benchmark-result fields.

## Continuation Rules

- Do not import producer code; integrate only through the artifact.
- Add schema versions rather than silently changing `1.0`.
- Keep producer latency separate from evaluator overhead.
- Preserve fail-fast exact ID parity before metrics.
- Add a RAG exporter and cross-repository CI test as the next integration slice.

## Remaining Gates

- Local tests, benchmark, and validator must pass after each change.
- Docker must execute the default artifact path.
- Status stays `benchmarked` until remote publication and CI evidence exist.
