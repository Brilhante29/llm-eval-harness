# Verification: llm-eval-harness

Date: `2026-07-21`

## Evidence

- Six unit tests passed, including duplicate IDs, missing/unexpected IDs, and unknown schema version failures.
- `tools/validate-project.ps1 -SkipDocker` passed.
- Docker image `llm-eval-harness:audit` built and executed successfully.
- The container evaluated a `rag-knowledge-base` artifact at F1 `0.5718` and EM `0.00`.
- CI checks out the producer SHA from `contracts/producers.lock.json`, runs retrieval, exports a fresh artifact, and evaluates it through the public contract.
- The result records producer project/version/run, artifact version, metric samples, command, timestamp, and environment.

## Remaining Risk

The committed artifact is deterministic and RAG-shaped but not exported by a live sibling CI job yet. Remote CI and an actual cross-repository producer run remain unverified.
