from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V1_PATH = ROOT / "benchmarks" / "results" / "llm-eval-baseline.json"
V2_PATH = ROOT / "benchmarks" / "publication" / "llm-eval-baseline-v2.json"
SCHEMA_PATH = ROOT / ".portfolio" / "contracts" / "benchmark-result-v2.schema.json"
CONFIG_PATH = ROOT / "benchmarks" / "config" / "llm-eval-baseline-v2.json"
FIXTURE_PATH = ROOT / "data" / "fixtures"
LOCK_PATH = ROOT / "requirements-validation.lock"
PRODUCER_PATH = ROOT / "tools" / "generate-publication-benchmark.py"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def load_producer() -> Any:
    spec = importlib.util.spec_from_file_location("publication_benchmark", PRODUCER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load publication producer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git_has_commit(commit: str) -> bool:
    completed = subprocess.run(
        ["git", "-c", f"safe.directory={ROOT}", "-C", str(ROOT), "cat-file", "-e", f"{commit}^{{commit}}"],
        capture_output=True,
        check=False,
    )
    return completed.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-git", action="store_true")
    args = parser.parse_args()

    manifest = (ROOT / "project.yaml").read_text(encoding="utf-8")
    published = re.search(r"(?m)^status:\s*published\s*$", manifest) is not None
    if not V2_PATH.is_file():
        require(not published, "published project requires V2 evidence")
        print("publication_evidence=not-applicable")
        return

    import jsonschema

    v1 = read_json(V1_PATH)
    v2 = read_json(V2_PATH)
    schema = read_json(SCHEMA_PATH)
    jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    ).validate(v2)

    require(v1.get("project") == "llm-eval-harness", "unexpected V1 project")
    require(v2.get("project") == "llm-eval-harness", "unexpected V2 project")
    require(v2.get("benchmark_id") == "artifact-f1-v1", "unexpected benchmark id")
    require(v1.get("metric") == "f1", "unexpected primary metric")
    require(v1.get("value") == v1.get("f1") == 0.8449, "unexpected F1 baseline")
    require(v1.get("exact_match") == 0.25, "unexpected exact-match baseline")
    require(v1.get("summary", {}).get("case_count") == 4, "expected four aligned cases")
    require(v1.get("environment", {}).get("producer_project") == "rag-knowledge-base", "unexpected producer")

    metric = v2["metrics"][0]
    require(metric["name"] == "f1", "unexpected V2 metric")
    require(metric["value"] == v1["value"], "V1/V2 value mismatch")
    require(metric["samples"] == v1["samples"], "V1/V2 samples mismatch")
    require(metric["failures"] == 0, "publication contains failures")
    require(v2["execution"]["repeat"] == v1["repeat"] == 1, "execution repeat mismatch")
    require(v2["workload"]["measured_iterations"] == 4, "measured workload must be four cases")
    require(v2["provenance"]["artifact_digest"] == sha256_file(V1_PATH), "raw artifact digest mismatch")
    require(re.fullmatch(r"sha256:[0-9a-f]{64}", v2["provenance"]["image_digest"]) is not None, "invalid image digest")

    config = read_json(CONFIG_PATH)
    require(v2["comparability_key"] == config["comparability_key"], "comparability key mismatch")
    require(config["measured_cases"] == 4, "publication config case count mismatch")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require("0.8449" in readme and "0.25" in readme, "README metrics do not match evidence")
    require(
        "result_path: benchmarks/publication/llm-eval-baseline-v2.json" in manifest,
        "manifest V2 path mismatch",
    )

    if args.require_git:
        source_commit = v2["provenance"]["source_commit"]
        require(git_has_commit(source_commit), "source commit unavailable; fetch full history")
        producer = load_producer()
        require(
            v2["workload"]["fixture_digest"]
            == producer.digest_committed_path(ROOT, FIXTURE_PATH, source_commit),
            "committed fixture digest mismatch",
        )
        require(
            v2["workload"]["config_digest"]
            == producer.digest_committed_path(ROOT, CONFIG_PATH, source_commit),
            "committed config digest mismatch",
        )
        require(
            v2["provenance"]["dependency_lock_digest"]
            == producer.digest_committed_path(ROOT, LOCK_PATH, source_commit),
            "committed validation-lock digest mismatch",
        )

    serialized = json.dumps({"v1": v1, "v2": v2})
    for forbidden in ("C:\\Users\\", "github" + "_pat_", "gh" + "p_"):
        require(forbidden not in serialized, f"forbidden value in evidence: {forbidden}")
    print("publication_evidence=passed")


if __name__ == "__main__":
    main()
