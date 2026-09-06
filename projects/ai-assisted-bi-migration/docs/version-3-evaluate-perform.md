# Version 3 — Evaluate and Improve Performance

After the workflow was useful and secure, two production questions remained:

1. Are the AI outputs actually useful?
2. Is the application fast enough to use?

## AI evaluation

RAGAS is used to evaluate the retrieval and answer side of the system across changes to prompts, models, chunking, and search settings.

The evaluation focuses on measures such as:

- Context recall
- Answer relevance
- Faithfulness

## Migration validation

The migrated reports are checked separately with deterministic comparisons:

- Row counts
- Aggregates
- Measures
- Filters
- Distinct counts
- Other business-critical values

A dashboard looking similar is not enough to declare a migration successful.

## Latency

The request path was reviewed as a whole rather than optimizing only the model call:

```text
Request
  -> retrieval
  -> context construction
  -> model call
  -> response delivery
```

Caching and SSE response streaming were used as part of the optimization work. The workload saw an improvement of approximately 250 ms at P95.

## Goal

Make the migration workflow measurable and practical for real users while keeping AI quality and data correctness visible.
