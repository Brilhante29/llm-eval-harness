# llm-eval-harness Specification

## Requirement: versioned producer boundary

The system SHALL accept prediction artifact version `1.0` from any producer without importing producer code.

## Requirement: complete case alignment

The system SHALL reject duplicate, missing, and unexpected case IDs before computing metrics.

### Scenario: missing and unexpected outputs

- GIVEN references contain `q1` and `q2`
- AND predictions contain `q1` and `q3`
- WHEN validation runs
- THEN it reports missing `q2` and unexpected `q3`
- AND no metrics are emitted

## Requirement: shared benchmark evidence

The result SHALL include project, metric, value, unit, timestamp, command, samples, and environment. Producer identity and schema version SHALL remain traceable.

## Requirement: latency separation

Producer latency SHALL come from the prediction artifact and SHALL NOT be represented as evaluator execution latency.
