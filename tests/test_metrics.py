import json
import tempfile
import unittest
from pathlib import Path

from llm_eval_harness.artifacts import (
    ArtifactValidationError,
    align_cases,
    load_prediction_artifact,
    load_references,
)
from llm_eval_harness.evaluator import evaluate
from llm_eval_harness.metrics import exact_match, token_f1

FIXTURES = Path("data/fixtures")


class MetricsTests(unittest.TestCase):
    def test_exact_match_normalizes_text(self):
        self.assertEqual(exact_match("Latency, in MS!", "latency in ms"), 1.0)

    def test_f1_and_cross_repository_artifact(self):
        references = load_references(FIXTURES / "references.jsonl")
        artifact = load_prediction_artifact(
            FIXTURES / "rag-predictions.v1.json"
        )
        result = evaluate(references, artifact)
        self.assertGreater(token_f1("grounded retrieved context", "retrieved context is grounded"), 0.7)
        self.assertEqual(result["project"], "llm-eval-harness")
        self.assertEqual(result["metric"], "f1")
        self.assertEqual(result["value"], result["f1"])
        self.assertEqual(result["unit"], "ratio")
        self.assertEqual(len(result["samples"]), 4)
        self.assertEqual(result["environment"]["producer_project"], "rag-knowledge-base")
        self.assertIn("timestamp", result)
        self.assertIn("command", result)

    def test_rejects_duplicate_reference_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "references.jsonl"
            path.write_text(
                '{"id":"q1","reference":"a"}\n'
                '{"id":"q1","reference":"b"}\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ArtifactValidationError, "duplicate reference id"):
                load_references(path)

    def test_rejects_duplicate_prediction_ids(self):
        artifact = self._fixture_artifact(
            [
                {"id": "q1", "prediction": "a"},
                {"id": "q1", "prediction": "b"},
            ]
        )
        with self.assertRaisesRegex(ArtifactValidationError, "duplicate prediction id"):
            self._load_temporary_artifact(artifact)

    def test_rejects_missing_and_unexpected_prediction_ids(self):
        references = {"q1": "one", "q2": "two"}
        artifact = self._fixture_artifact(
            [
                {"id": "q1", "prediction": "one"},
                {"id": "q3", "prediction": "three"},
            ]
        )
        with self.assertRaisesRegex(
            ArtifactValidationError,
            "missing prediction ids.*unexpected prediction ids",
        ):
            align_cases(references, artifact)

    def test_rejects_unknown_artifact_version(self):
        artifact = self._fixture_artifact([{"id": "q1", "prediction": "a"}])
        artifact["schema_version"] = "2.0"
        with self.assertRaisesRegex(ArtifactValidationError, "schema_version"):
            self._load_temporary_artifact(artifact)

    def test_rejects_created_at_without_timezone(self):
        artifact = self._fixture_artifact([{"id": "q1", "prediction": "a"}])
        artifact["created_at"] = "2026-07-21T00:00:00"
        with self.assertRaisesRegex(ArtifactValidationError, "UTC offset"):
            self._load_temporary_artifact(artifact)

    @staticmethod
    def _fixture_artifact(predictions):
        return {
            "schema_version": "1.0",
            "producer": {
                "project": "test-producer",
                "version": "0.1.0",
                "run_id": "test-run",
            },
            "created_at": "2026-07-21T00:00:00Z",
            "predictions": predictions,
        }

    @staticmethod
    def _load_temporary_artifact(artifact):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "predictions.json"
            path.write_text(json.dumps(artifact), encoding="utf-8")
            return load_prediction_artifact(path)


if __name__ == "__main__":
    unittest.main()
