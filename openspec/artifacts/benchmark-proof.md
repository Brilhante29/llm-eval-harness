# Benchmark Proof: llm-eval-harness

## Primary Metric

- Metric: `f1`
- Unit: `ratio`
- Result: `0.8449`
- Exact match: `0.25`
- Producer: `rag-knowledge-base@0.1.0`
- Artifact schema: `1.0`
- Result path: `benchmarks/results/llm-eval-baseline.json`

## Command

    python -m llm_eval_harness benchmark --references data/fixtures/references.jsonl --predictions data/fixtures/rag-predictions.v1.json --output benchmarks/results/llm-eval-baseline.json

## Interpretation

The score comes from four committed producer predictions joined to four independent references by exact ID parity. Average producer latency is `7.675 ms` in the fixture and is reported separately from local evaluator overhead.
