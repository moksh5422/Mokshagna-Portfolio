# Agent Design

The demo uses a small set of focused components rather than one large autonomous agent.

## Discovery Agent

Creates the initial report inventory. It is deterministic because metadata extraction does not require model judgment.

Output:

- sources
- calculation count
- transformation count
- filters
- dependencies

## Planner Agent

Turns inventory into a simple complexity score. A production version can add dependency depth, data sensitivity, business criticality, and migration risk.

## Migration Agent

This is the main LLM-backed component. It interprets legacy expressions and proposes where the logic should move:

- Fabric transformation
- semantic model
- report-level logic
- human review

Every proposal carries confidence and can be rejected by the review process.

## Security Agent

Applies a role/scope policy before an AI or tool request is allowed. The model is never the authority for authorization.

## PII Agent

Looks for common sensitive field names before content is passed to an AI path. A production implementation would combine this with structured classification and value-level scanning.

## Similarity Agent

Finds repeated expressions across reports. This creates opportunities to consolidate duplicated business logic into reusable Fabric transformations or semantic-model measures.

## Evaluation Agent

Applies confidence thresholds and review flags. The production version should additionally connect to a RAGAS evaluation suite and regression dataset.

## MCP Tool Registry

Represents the controlled tool surface available to an agent. Example operations include:

```text
list_report_dependencies()
get_transformation()
get_sample_data()
validate_report()
submit_for_review()
```

Each tool should be authorized independently. The agent should not have unrestricted database or API access.

## Deterministic Reconciliation

This is intentionally outside the LLM. It compares source and target metrics such as row counts, aggregates, measures, filters, and distinct counts.

## Orchestration rule

The overall design follows one rule:

> Use the model for interpretation; use code for guarantees.

This keeps the workflow useful without making the LLM responsible for permissions or the final migration decision.
