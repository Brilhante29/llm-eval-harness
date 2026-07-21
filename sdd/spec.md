# Spec: 2 - llm-eval-harness

## Claim

Evaluate versioned RAG/LLM prediction artifacts with strict case alignment, exact match, token F1, and separated producer/evaluator latency.

## Acceptance Criteria

- Accepts a `prediction-artifact/1.0` JSON from any producer repository.
- Loads references independently from predictions.
- Rejects duplicate reference IDs, duplicate prediction IDs, missing IDs, unexpected IDs, invalid types, and unknown schema versions.
- Emits the shared top-level benchmark-result fields plus producer and artifact identity.
- Runs locally and in Docker without credentials or access to the producer runtime.
