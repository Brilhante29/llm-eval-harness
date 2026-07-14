import unittest
from llm_eval_harness.cli import evaluate, load_cases
from llm_eval_harness.metrics import exact_match, token_f1

class MetricsTests(unittest.TestCase):
    def test_exact_match_normalizes_text(self):
        self.assertEqual(exact_match("Latency, in MS!", "latency in ms"), 1.0)

    def test_f1_and_eval_are_high_enough(self):
        self.assertGreater(token_f1("grounded retrieved context", "retrieved context is grounded"), 0.7)
        result = evaluate(load_cases())
        self.assertGreaterEqual(result["f1"], 0.75)
        self.assertIn("avg_latency_ms", result)

if __name__ == "__main__":
    unittest.main()
