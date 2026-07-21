# Prediction Artifact Contract

`prediction-artifact.schema.json` is the file boundary between answer producers and this evaluator.

A RAG service writes one versioned JSON object containing producer identity, a run ID, creation time, and predictions keyed by evaluation-case ID. The harness imports only that file; neither repository imports the other's code.

Version `1.0` requires exact ID parity with the selected reference set. Duplicate, missing, and unexpected IDs fail before metrics are computed. Producers may add context IDs and metadata without changing the evaluator.
