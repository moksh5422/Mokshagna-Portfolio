# Version 1 — Understand the Legacy Workload

The first problem was not report rendering. It was understanding what each legacy report actually depended on.

For the 81-report migration, the workflow starts by turning report definitions into structured information: sources, tables, columns, calculations, filters, relationships, and transformations.

An LLM can then help with the parts that need interpretation, such as explaining an unfamiliar expression, suggesting an equivalent target transformation, or flagging a dependency that looks ambiguous.

The model output is a proposal, not an acceptance decision.

## Goal

Reduce repetitive discovery work while keeping migration decisions reviewable.

## Output

```text
Report
  -> source inventory
  -> dependency map
  -> calculation map
  -> transformation map
  -> migration specification
```
