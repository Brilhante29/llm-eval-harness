# Change Proposal: baseline

Project: `llm-eval-harness` (#2)

## Intent

Local-first evaluation harness for LLM/RAG answers with exact match, token F1, and reproducible latency benchmark.

## Why This Change Exists

Describe the smallest change that improves the measurable claim or removes a
known portfolio risk.

## Scope

- In scope: <scope>
- Out of scope: paid credentials, unrelated infrastructure, and unmeasured features.

## Portfolio Impact

Program: `ai-evaluation-retrieval`

This change should produce evidence, fixtures, decisions, or components that
can be reused by sibling repositories without moving project-specific behavior
into the kit.

## Acceptance Signal

The benchmark in `project.yaml` remains reproducible and its result is recorded
in `benchmarks/results/`.
