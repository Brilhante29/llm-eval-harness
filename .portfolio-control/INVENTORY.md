# Portfolio Control: #2 llm-eval-harness

## Identity

- **Program:** AI Evaluation and Retrieval Systems
- **Status:** published
- **Proves:** contract-first evaluation of answer artifacts with strict producer identity and case alignment
- **Primary benchmark:** `f1 = 0.5718`

## Evidence Map

| Evidence | Location | State |
|---|---|---|
| Specification | `sdd/spec.md` | complete |
| Architecture decision | `sdd/architecture-decision.md` | complete |
| Benchmark plan | `sdd/benchmark-plan.md` | complete |
| Raw benchmark | `benchmarks/results/llm-eval-baseline.json` | versioned |
| Publication benchmark | `benchmarks/publication/llm-eval-baseline-v2.json` | provenance validated |
| Producer lock | `contracts/producers.lock.json` | RAG SHA pinned |
| OpenSpec verification | `openspec/artifacts/verification.md` | complete |
| Reuse review | `sdd/reuse-improvement-review.md` | complete |

This file is the project-level inventory. Update it whenever a new proof artifact, reusable component, or architectural decision appears.
