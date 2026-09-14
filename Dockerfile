FROM python:3.12.14-slim-trixie@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea

RUN apt-get update && apt-get upgrade --yes && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY contracts ./contracts
COPY data ./data
COPY benchmarks ./benchmarks

RUN pip install --no-cache-dir --no-deps .

ENTRYPOINT ["python", "-m", "llm_eval_harness"]
CMD ["benchmark", "--references", "data/fixtures/references.jsonl", "--predictions", "data/fixtures/rag-predictions.v1.json", "--output", "benchmarks/results/llm-eval-baseline.json"]
