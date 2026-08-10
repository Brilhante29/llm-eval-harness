# #2 llm-eval-harness: F1 = 0.84

Local-first evaluation harness for LLM/RAG answers with exact match, token F1, and reproducible latency benchmark.

This repository belongs to the AI Evaluation and Retrieval Systems program. Its job is narrow: prove the measurable claim through the selected component pack before adding unrelated infrastructure or features.

The benchmark is the proof. F1 = 0.5718 and exact match = 0.00 over four cases exported by pinned `rag-knowledge-base` retrieval. V2 provenance is stored in `benchmarks/publication/llm-eval-baseline-v2.json`; evaluator timing remains environment-specific in the raw artifact.

The important architecture decision is clean-architecture. The metric and benchmark use cases must stay independent from CLI, fixtures, and future providers.

The default path stays local-first. The project uses python, exposes cli-first, uses messaging mode `none`, and stores data with `fixture-files`. The dependency rule is explicit: Domain metrics and application benchmark orchestration do not import interface code.

The rejected work matters as much as the implemented work. Anything that does not improve the benchmark stays out of the first version.

Post angle: start with the number, show the architecture boundary, then explain which future adapter can be added without changing the core use cases.
