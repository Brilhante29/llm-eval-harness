# Intent: llm-eval-harness

## Measurable Claim

Local-first evaluation harness for LLM/RAG answers with exact match, token F1, and reproducible latency benchmark.

## Problem

Defines the objective answer-quality measurement layer used by the AI Evaluation and RAG Platform.

## In Scope

- Use the selected component pack: `ai-evaluation-retrieval`.
- Keep the project under the AI Evaluation and Retrieval Systems program.
- Preserve the benchmark contract: `f1` in `benchmarks/results/llm-eval-baseline.json`.
- Keep the default path local-first and reproducible.

## Out Of Scope

- Paid credentials for the default demo.
- External infrastructure that is not required by the benchmark.
- Replacing local portfolio skills with external components silently.

## Default Demo Path

- Status: benchmarked
- Runtime: python-cli
- Benchmark command: `python -m llm_eval_harness benchmark --output benchmarks/results/llm-eval-baseline.json`

## Public Proof

- Benchmark: F1 = 0.84
- Result path: `benchmarks/results/llm-eval-baseline.json`
