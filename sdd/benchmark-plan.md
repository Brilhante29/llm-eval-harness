# Benchmark Plan

Primary metric: `f1`.

Command:

```powershell
python -m llm_eval_harness benchmark --references data/fixtures/references.jsonl --predictions data/fixtures/rag-predictions.v1.json --output benchmarks/results/llm-eval-baseline.json
```

The gate first requires exact ID parity between references and predictions. It then computes one EM and token-F1 sample per case and macro-averages each metric. Producer latency comes from the producer artifact; evaluator latency measures only local normalization and metric calculation.

The four-case fixture is a regression baseline. A production evaluation needs a larger reviewed dataset and confidence intervals.
