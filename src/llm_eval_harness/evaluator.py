from __future__ import annotations

import platform
import sys
import time
from datetime import datetime, timezone

from .artifacts import align_cases
from .metrics import exact_match, token_f1

DEFAULT_COMMAND = (
    "python -m llm_eval_harness benchmark "
    "--references data/fixtures/references.jsonl "
    "--predictions data/fixtures/rag-predictions.v1.json "
    "--output benchmarks/results/llm-eval-baseline.json"
)


def evaluate(references: dict[str, str], artifact: dict, command: str = DEFAULT_COMMAND) -> dict:
    cases = align_cases(references, artifact)
    started = time.perf_counter()
    rows = []
    for case in cases:
        em = exact_match(case["prediction"], case["reference"])
        f1 = token_f1(case["prediction"], case["reference"])
        row = {"id": case["id"], "exact_match": em, "f1": f1}
        if case["latency_ms"] is not None:
            row["producer_latency_ms"] = case["latency_ms"]
        rows.append(row)
    evaluator_latency_ms = (time.perf_counter() - started) * 1000 / len(rows)

    exact_match_value = round(
        sum(row["exact_match"] for row in rows) / len(rows), 4
    )
    f1_value = round(sum(row["f1"] for row in rows) / len(rows), 4)
    producer_latencies = [
        row["producer_latency_ms"]
        for row in rows
        if "producer_latency_ms" in row
    ]
    summary = {
        "case_count": len(rows),
        "exact_match": exact_match_value,
        "f1": f1_value,
        "avg_evaluator_latency_ms": round(evaluator_latency_ms, 4),
    }
    if producer_latencies:
        summary["avg_producer_latency_ms"] = round(
            sum(producer_latencies) / len(producer_latencies), 4
        )

    producer = artifact["producer"]
    return {
        "project": "llm-eval-harness",
        "metric": "f1",
        "value": f1_value,
        "unit": "ratio",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "command": command,
        "repeat": 1,
        "samples": [row["f1"] for row in rows],
        "summary": summary,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "implementation": sys.implementation.name,
            "producer_project": producer["project"],
            "producer_version": producer["version"],
            "producer_run_id": producer["run_id"],
            "prediction_artifact_schema": artifact["schema_version"],
        },
        "primary_metric": "f1",
        "exact_match": exact_match_value,
        "f1": f1_value,
        "avg_evaluator_latency_ms": summary["avg_evaluator_latency_ms"],
        "producer": producer,
        "prediction_artifact": {
            "schema_version": artifact["schema_version"],
            "created_at": artifact["created_at"],
        },
        "cases": rows,
    }
