# AI-Assisted BI Migration

A practical engineering pattern for migrating legacy BI workloads to Power BI and Microsoft Fabric when the difficult part is understanding the existing logic, not recreating the charts.

This project is based on an enterprise migration pattern involving **81 Spotfire reports**, multiple upstream data sources, legacy transformations, calculated fields, filters, business rules, and a move to Power BI and Microsoft Fabric.

This repository is intentionally sanitized: it contains no client data, proprietary report definitions, credentials, or confidential implementation details. The examples are synthetic and demonstrate the engineering approach.

## The problem

A report migration can look simple from a distance:

```text
Open report -> rebuild in Power BI -> test -> repeat
```

That becomes difficult when every report has different dependencies and some important logic is buried inside legacy expressions or transformations.

The real questions become:

- What data sources does this report depend on?
- Where is each transformation happening today?
- Is the calculation report logic or data logic?
- Can the same business rule be reused by other reports?
- Does the new report produce the same numbers?
- Which parts can be automated safely, and which need an engineer to review?

## Approach

The migration is treated as a repeatable engineering workflow rather than 81 separate dashboard rebuilds.

```text
Legacy Reports
      |
      v
Report Inventory + Parsing
      |
      +-------------------------+
      |                         |
      v                         v
Deterministic Analysis      LLM-assisted Analysis
      |                    - formula interpretation
      |                    - transformation mapping
      |                    - ambiguity detection
      +------------+------------+
                   |
                   v
             Migration Spec
                   |
                   v
              Human Review
                   |
                   v
          Fabric Transformation
                   |
                   v
            Curated Data Layer
                   |
                   v
          Power BI Semantic Model
                   |
                   v
             Power BI Report
                   |
                   v
             Reconciliation
                   |
           +-------+-------+
           |               |
           v               v
         PASS          REVIEW
```

## Where AI is useful

The LLM is used where interpretation helps:

- Explaining unfamiliar legacy expressions
- Suggesting an equivalent target transformation
- Grouping similar calculations
- Detecting potentially ambiguous business logic
- Producing a first-pass migration note

The model is **not** treated as the final authority.

A proposed mapping can carry a confidence score and a review reason. Low-confidence or ambiguous cases are sent to an engineer rather than being silently accepted.

## Where deterministic code is preferred

Some parts of the migration should remain predictable:

- Metadata extraction
- Source/dependency inventory
- PII checks
- Data-quality checks
- Reconciliation
- Acceptance criteria
- Migration status tracking

This keeps the AI in a supporting role while important acceptance decisions remain testable.

## Example migration record

A synthetic report definition can describe a metric like this:

```json
{
  "report": "sales-overview",
  "metric": "Revenue",
  "legacy_expression": "SUM(SalesAmount)",
  "target_layer": "semantic_model",
  "proposed_expression": "SUM(FactSales[SalesAmount])",
  "confidence": 0.97,
  "status": "READY_FOR_REVIEW"
}
```

For an ambiguous rule, the system should make the uncertainty visible:

```json
{
  "report": "customer-analysis",
  "metric": "Customer Segment",
  "target_layer": "fabric-transformation",
  "status": "REVIEW_REQUIRED",
  "reason": "Legacy logic refers to an unmapped customer type"
}
```

## Validation

The migration should not be accepted because the dashboard looks similar.

The validation layer can compare:

- Row counts
- Totals and aggregates
- Distinct counts
- Filter behavior
- Null handling
- Dimension membership
- Important business measures

Example:

```text
Report: sales-overview

Rows
Legacy : 1,245,883
Target : 1,245,883
Status : PASS

Revenue
Legacy : 84,392,112
Target : 84,392,109
Status : REVIEW

Region Filter
Legacy : EMEA
Target : EMEA
Status : PASS
```

A small difference should be surfaced for investigation instead of being hidden by an AI-generated explanation.

## Security

An enterprise implementation should not expose sensitive report content or PII to an unapproved model endpoint.

The production pattern should include approved model endpoints, identity-based access, RBAC, secret management, PII detection/redaction, controlled tool access, logging, and input/output validation.

## Project structure

```text
ai-assisted-bi-migration/
├── README.md
├── LINKEDIN_POST.md
├── docs/
│   └── migration-workflow.md
├── examples/
│   └── legacy_report.json
└── src/
    └── validate/
        └── reconciliation.py
```

## What this project demonstrates

> Turn 81 individual migrations into one repeatable migration workflow with 81 inputs.

The value is not the LLM by itself. It comes from combining AI-assisted interpretation with data engineering, validation, security, human review, and a clear separation between source data, transformations, semantic modelling, and reporting.
