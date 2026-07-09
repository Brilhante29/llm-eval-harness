# #2 llm-eval-harness

**Status:** scaffold

**Proves:** avaliacao objetiva de RAG/LLM.

**Benchmark target:** exact_match, f1, latency_ms.

**Stack:** python, typer, pydantic, pytest, docker.

## Next milestone

Implement the smallest Docker-runnable version and produce the first JSON benchmark under enchmarks/results/.

## Run

`ash
docker build -t llm-eval-harness .
docker run --rm llm-eval-harness
`

## Benchmark

`ash
docker run --rm llm-eval-harness benchmark
`

| Metric | Value | Unit |
|---|---:|---|
| exact_match, f1, latency_ms | pending | pending |

## Architecture

Defined in sdd/spec.md before implementation.

## References

See REFERENCES.md.