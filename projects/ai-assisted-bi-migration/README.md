# Legacy BI Migration Intelligence

**Niche problem:** how can AI help engineers understand and migrate poorly documented legacy BI logic without losing enterprise access controls, confidence in the migrated numbers, or acceptable response time?

This project documents a sanitized version of an enterprise migration pattern involving **81 Spotfire reports**, multiple upstream data sources, legacy transformations, calculated fields, filters, and business rules, with the target platform being **Power BI and Microsoft Fabric**.

The interesting part was not recreating charts. It was building a repeatable way to reason about the old system, protect the information used by the workflow, evaluate AI-assisted decisions, and validate the final result.

> This repository contains synthetic examples only. No client data, proprietary report definitions, credentials, or confidential implementation details are included.

## Three versions of the solution

### V1 — Understand the legacy workload

The first bottleneck was discovery.

Before rebuilding a report, the workflow builds a structured view of its sources, tables, calculations, filters, relationships, and transformations.

The LLM is used for interpretation tasks such as:

- explaining unfamiliar legacy expressions
- suggesting an equivalent target transformation
- grouping similar calculations
- flagging ambiguous dependencies

The model produces a proposal. It does not decide whether the migration is correct.

`legacy report -> inventory -> dependency map -> transformation map -> migration spec`

### V2 — Secure the workflow

Once AI was reading enterprise information, access control became a first-class problem.

The security boundary stays in the application rather than the model. Identity and RBAC determine what the caller is allowed to access before an AI or tool request is executed.

The design also considers:

- PII detection and redaction
- approved model endpoints
- secret management
- controlled tool/data access
- input/output guardrails
- audit-friendly request paths

`identity -> authorization -> allowed operation -> AI/tool request`

### V3 — Evaluate and improve performance

The next questions were whether the AI was actually helping and whether users could work with the system quickly enough.

For the AI side, **RAGAS** is used to evaluate retrieval and answer quality as prompts, models, chunking, and search settings change. Metrics include context recall, answer relevance, and faithfulness.

For the migration side, deterministic reconciliation checks compare source and target values such as row counts, aggregates, measures, filters, and distinct counts.

Latency is considered across the full path:

`request -> retrieval -> context construction -> model call -> response delivery`

Caching and **SSE streaming** were used as part of the performance work, with an improvement of approximately **250 ms at P95** in the workload described here.

## Target architecture

```text
Legacy Spotfire Reports
          |
          v
   Inventory + Parsing
          |
     +----+----+
     |         |
     v         v
Deterministic  LLM-assisted
Analysis       Interpretation
     |         |
     +----+----+
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
      Validation
       /       \
     PASS     REVIEW
```

## What the project demonstrates

The core idea is simple:

> **Turn 81 individual migrations into one repeatable engineering workflow with 81 inputs.**

AI is one part of the system. The useful outcome comes from combining AI-assisted interpretation with data engineering, RBAC, PII controls, evaluation, deterministic validation, performance work, and human review.

## Repository structure

```text
ai-assisted-bi-migration/
├── README.md
├── LINKEDIN_POST.md
├── docs/
│   ├── version-1-understand.md
│   ├── version-2-secure.md
│   └── version-3-evaluate-perform.md
├── examples/
│   └── legacy_report.json
└── src/
    └── validate/
        └── reconciliation.py
```
