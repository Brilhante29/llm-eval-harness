# Spec: 2 - llm-eval-harness

## Claim

Local-first evaluation harness for LLM/RAG answers with exact match, token F1, and reproducible latency benchmark.

## Acceptance Criteria

- Runs locally with `python -m llm_eval_harness benchmark --output benchmarks/results/llm-eval-baseline.json`.
- Runs in Docker with no paid secret.
- Writes benchmark JSON under `benchmarks/results/`.
- Keeps domain/evaluation logic independent from CLI and future providers.
