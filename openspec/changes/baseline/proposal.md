# Change Proposal: artifact-driven-evaluation

Project: `llm-eval-harness` (#2)

## Intent

Replace the combined local answer fixture with a versioned producer artifact that a RAG or LLM repository can emit without code coupling.

## Scope

- In scope: prediction schema `1.0`, producer identity, strict case-ID alignment, EM/F1, separated latency, shared result contract, and tests.
- Out of scope: live paid inference, queues, hosted evaluation services, and changing producer implementations.

## Portfolio Impact

Program: `ai-evaluation-retrieval`.

The JSON schema creates the first executable cross-repository boundary between answer producers and the evaluation layer.

## Acceptance Signal

A RAG-shaped artifact evaluates successfully, invalid versions and ID mismatches fail, and the benchmark emits all shared result fields.
