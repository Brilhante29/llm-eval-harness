# Verification: llm-eval-harness

Date: `2026-07-21`

## Evidence

- Six unit tests passed, including duplicate IDs, missing/unexpected IDs, and unknown schema version failures.
- `tools/validate-project.ps1 -SkipDocker` passed.
- Docker image `llm-eval-harness:audit` built and executed successfully.
- The container evaluated the `rag-knowledge-base` fixture at F1 `0.8449` and EM `0.25`.
- The result records producer project/version/run, artifact version, metric samples, command, timestamp, and environment.

## Remaining Risk

The committed artifact is deterministic and RAG-shaped but not exported by a live sibling CI job yet. Remote CI and an actual cross-repository producer run remain unverified.
