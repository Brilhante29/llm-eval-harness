FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY contracts ./contracts
COPY data ./data
COPY benchmarks ./benchmarks

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "llm_eval_harness"]
CMD ["benchmark", "--references", "data/fixtures/references.jsonl", "--predictions", "data/fixtures/rag-predictions.v1.json", "--output", "benchmarks/results/llm-eval-baseline.json"]
