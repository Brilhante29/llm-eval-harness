import argparse
import json
from pathlib import Path

from .artifacts import load_prediction_artifact, load_references
from .evaluator import evaluate

DEFAULT_REFERENCES = Path("data/fixtures/references.jsonl")
DEFAULT_PREDICTIONS = Path("data/fixtures/rag-predictions.v1.json")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["benchmark"], nargs="?", default="benchmark")
    parser.add_argument("--references", type=Path, default=DEFAULT_REFERENCES)
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("benchmarks/results/llm-eval-baseline.json"),
    )
    args = parser.parse_args()
    command = (
        "python -m llm_eval_harness benchmark "
        f"--references {args.references.as_posix()} "
        f"--predictions {args.predictions.as_posix()} "
        f"--output {args.output.as_posix()}"
    )
    result = evaluate(
        load_references(args.references),
        load_prediction_artifact(args.predictions),
        command,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
