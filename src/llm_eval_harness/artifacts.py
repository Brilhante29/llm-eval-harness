from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

PREDICTION_ARTIFACT_VERSION = "1.0"


class ArtifactValidationError(ValueError):
    pass


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ArtifactValidationError(
                f"{path}:{line_number} is not valid JSON: {error.msg}"
            ) from error
        if not isinstance(row, dict):
            raise ArtifactValidationError(f"{path}:{line_number} must be an object")
        rows.append(row)
    if not rows:
        raise ArtifactValidationError(f"artifact is empty: {path}")
    return rows


def load_references(path: Path) -> dict[str, str]:
    references: dict[str, str] = {}
    for row in _read_jsonl(path):
        case_id = row.get("id")
        reference = row.get("reference")
        if not isinstance(case_id, str) or not case_id:
            raise ArtifactValidationError("each reference must have a non-empty string id")
        if case_id in references:
            raise ArtifactValidationError(f"duplicate reference id: {case_id}")
        if not isinstance(reference, str) or not reference:
            raise ArtifactValidationError(
                f"reference {case_id} must have non-empty text"
            )
        references[case_id] = reference
    return references


def load_prediction_artifact(path: Path) -> dict:
    try:
        artifact = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ArtifactValidationError(
            f"{path} is not valid JSON: {error.msg}"
        ) from error
    if not isinstance(artifact, dict):
        raise ArtifactValidationError("prediction artifact must be an object")
    if artifact.get("schema_version") != PREDICTION_ARTIFACT_VERSION:
        raise ArtifactValidationError(
            "prediction artifact schema_version must be "
            f"{PREDICTION_ARTIFACT_VERSION}"
        )

    producer = artifact.get("producer")
    if not isinstance(producer, dict):
        raise ArtifactValidationError("prediction artifact must declare producer")
    for field in ("project", "version", "run_id"):
        if not isinstance(producer.get(field), str) or not producer[field]:
            raise ArtifactValidationError(f"producer.{field} must be a non-empty string")
    created_at = artifact.get("created_at")
    if not isinstance(created_at, str) or not created_at:
        raise ArtifactValidationError("created_at must be a non-empty string")
    try:
        parsed_created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as error:
        raise ArtifactValidationError("created_at must be an ISO 8601 timestamp") from error
    if parsed_created_at.tzinfo is None:
        raise ArtifactValidationError(
            "created_at must include a UTC offset or Z suffix"
        )

    predictions = artifact.get("predictions")
    if not isinstance(predictions, list) or not predictions:
        raise ArtifactValidationError("predictions must be a non-empty array")
    seen: set[str] = set()
    for row in predictions:
        if not isinstance(row, dict):
            raise ArtifactValidationError("each prediction must be an object")
        case_id = row.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise ArtifactValidationError("each prediction must have a non-empty string id")
        if case_id in seen:
            raise ArtifactValidationError(f"duplicate prediction id: {case_id}")
        seen.add(case_id)
        if not isinstance(row.get("prediction"), str):
            raise ArtifactValidationError(
                f"prediction {case_id} must contain a string prediction"
            )
        latency_ms = row.get("latency_ms")
        if latency_ms is not None and (
            not isinstance(latency_ms, (int, float))
            or isinstance(latency_ms, bool)
            or latency_ms < 0
        ):
            raise ArtifactValidationError(
                f"prediction {case_id} latency_ms must be non-negative"
            )
    return artifact


def align_cases(references: dict[str, str], artifact: dict) -> list[dict]:
    predictions = {row["id"]: row for row in artifact["predictions"]}
    expected_ids = set(references)
    actual_ids = set(predictions)
    missing = sorted(expected_ids - actual_ids)
    unexpected = sorted(actual_ids - expected_ids)
    if missing or unexpected:
        details = []
        if missing:
            details.append(f"missing prediction ids: {missing}")
        if unexpected:
            details.append(f"unexpected prediction ids: {unexpected}")
        raise ArtifactValidationError("; ".join(details))

    return [
        {
            "id": case_id,
            "reference": reference,
            "prediction": predictions[case_id]["prediction"],
            "latency_ms": predictions[case_id].get("latency_ms"),
        }
        for case_id, reference in references.items()
    ]
