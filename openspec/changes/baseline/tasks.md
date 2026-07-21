# Change Tasks: artifact-driven-evaluation

## Planning

- [x] Define the producer/evaluator contract boundary.
- [x] Record fail-fast ID parity semantics.
- [x] Separate producer and evaluator latency.

## Implementation

- [x] Add prediction artifact schema version `1.0`.
- [x] Split independent references from RAG-shaped predictions.
- [x] Reject duplicates, missing IDs, unexpected IDs, and unknown versions.
- [x] Emit shared result fields, producer identity, samples, and environment.
- [x] Update README, SDD, OpenSpec, tests, and baseline.

## Verification

- [x] Run compile and six unit tests.
- [x] Run `tools/validate-project.ps1 -SkipDocker`.
- [x] Build and execute `llm-eval-harness:audit`.
- [ ] Run `openspec validate --strict` when the CLI is installed.
- [ ] Verify remote CI after publication.
