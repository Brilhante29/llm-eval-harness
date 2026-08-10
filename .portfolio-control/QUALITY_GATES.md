# Quality Gates: #2 llm-eval-harness

Completion requires evidence, not intent.

- [x] README opens with `#2 llm-eval-harness` and reports the current benchmark number.
- [x] `project.yaml` names the problem, architecture, stack, primary metric, and result path.
- [x] SDD and OpenSpec artifacts agree with the implementation.
- [x] Metric code is isolated from producer, transport, persistence, and provider details.
- [x] SOLID, DRY, KISS, YAGNI, and coupling decisions are explicit.
- [x] Nine tests cover contracts, alignment, metrics, and malformed artifacts.
- [x] Docker executes the benchmark from a clean source commit.
- [x] CI executes the pinned RAG producer-consumer contract without secrets.
- [x] V1 and V2 evidence are generated from measured execution.
- [x] README, benchmark JSON, and `project.yaml` report F1 consistently.
- [x] The prediction schema was promoted to the reuse kit after its second adopter.
- [x] Independent audit blockers were addressed before default-branch publication.

Each new release still requires central exact-head GitHub Actions evidence.
