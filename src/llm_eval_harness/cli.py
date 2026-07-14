import argparse
import json
import time
from pathlib import Path
from .metrics import exact_match, token_f1

FIXTURE = Path("data/fixtures/eval_cases.jsonl")

def load_cases(path: Path = FIXTURE) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def evaluate(cases: list[dict]) -> dict:
    started = time.perf_counter()
    rows = []
    for case in cases:
        em = exact_match(case["prediction"], case["reference"])
        f1 = token_f1(case["prediction"], case["reference"])
        rows.append({"id": case["id"], "exact_match": em, "f1": f1})
    latency_ms = (time.perf_counter() - started) * 1000 / max(len(cases), 1)
    return {
        "project": "llm-eval-harness",
        "primary_metric": "f1",
        "exact_match": round(sum(r["exact_match"] for r in rows) / len(rows), 4),
        "f1": round(sum(r["f1"] for r in rows) / len(rows), 4),
        "avg_latency_ms": round(latency_ms, 4),
        "cases": rows,
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["benchmark"], nargs="?", default="benchmark")
    parser.add_argument("--output", default="benchmarks/results/llm-eval-baseline.json")
    args = parser.parse_args()
    result = evaluate(load_cases())
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
