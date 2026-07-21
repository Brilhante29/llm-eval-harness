# Architecture Decision

Decision: contract-bound evaluation pipeline with file-based ports.

Rationale: producer execution and evaluation have different ownership and failure modes. A versioned JSON artifact decouples them while preserving producer version, run ID, per-case IDs, optional context IDs, and latency. Validation completes before metric computation, preventing partial joins from becoming benchmark evidence.

Dependency direction:

- CLI depends on artifact loading and evaluator modules.
- Evaluator depends on pure metrics and aligned in-memory cases.
- Producer repositories depend only on the JSON schema, never this Python package.

Rejected:

- Combined prediction/reference fixture: it cannot prove cross-repository integration or detect missing producer output.
- Direct RAG package import: it couples release cycles and stacks.
- Queue or hosted evaluation service: unnecessary for the deterministic baseline.
