# Legacy BI Migration Intelligence

**Niche problem:** how can AI help engineers understand and migrate poorly documented legacy BI logic without making the model responsible for security, correctness, or production performance?

This project documents a sanitized enterprise migration pattern involving **81 Spotfire reports**, multiple upstream sources, legacy transformations, calculated fields, filters, and business rules, with **Power BI and Microsoft Fabric** as the target platform.

The goal is not to make an LLM “migrate dashboards.” The goal is to build a workflow that reduces repetitive investigation while keeping permissions, validation, and release decisions under engineering control.

> This repository contains synthetic examples only. No client data, proprietary report definitions, credentials, or confidential implementation details are included.

## Three versions of the solution

### V1 — Understand the legacy workload

Before rebuilding a report, the workflow creates a structured inventory of sources, tables, calculations, filters, relationships, and transformations.

An LLM is used where interpretation is useful: explaining unfamiliar expressions, suggesting target transformations, grouping similar logic, and flagging ambiguity.

The model produces a proposal. It does not decide whether the migration is correct.

`legacy report -> discovery -> dependency map -> transformation map -> migration spec`

### V2 — Secure the workflow

Once AI is working with enterprise information, the first production concern is access.

The application enforces identity and **RBAC** before AI or tool calls are allowed. PII scanning and redaction can be applied before information enters an AI processing path. Tool access is exposed through an allow-list rather than unrestricted model access.

`identity -> authorization -> PII check -> allowed operation -> AI/tool`

### V3 — Evaluate and improve performance

The workflow needs evidence that the AI is useful and that the final system behaves correctly.

**RAGAS** is used for retrieval/answer evaluation across changes to prompts, models, chunking, and search settings. The migration itself uses deterministic reconciliation for row counts, aggregates, measures, filters, and distinct counts.

Latency is treated as a full request-path problem:

`request -> retrieval -> context -> model -> response`

Caching and **SSE streaming** are part of the performance approach; the workload described here saw approximately **250 ms improvement at P95**.

## Working VS Code demo

The `demo/` folder now shows a fuller orchestration pattern. Some components are deterministic by design; the migration interpretation step can use Azure OpenAI when configured and falls back to local rules so the project still runs in VS Code without credentials.

### Agents and controls

| Component | Responsibility | AI or deterministic |
|---|---|---|
| Discovery Agent | Inventory sources, calculations, filters, transformations and dependencies | Deterministic |
| Planner Agent | Estimate migration complexity and prioritize work | Deterministic in demo |
| Migration Agent | Interpret legacy expressions and propose target-layer mappings | LLM + deterministic fallback |
| Security Agent | Enforce role/scope permissions before operations | Deterministic |
| PII Agent | Detect likely sensitive field names before AI processing | Deterministic |
| Similarity Agent | Find repeated calculations that may be reusable | Deterministic |
| Evaluation Agent | Apply confidence and review thresholds | Deterministic |
| MCP Tool Registry | Allow-list the operations an agent could request | Deterministic |
| Reconciliation | Compare source and target values | Deterministic |

### Demo flow

```text
Legacy Report
     |
     v
Discovery Agent
     |
     v
Planner Agent
     |
     v
Migration Agent
  + proposes mappings
  + returns confidence
     |
     +------------------+
     |                  |
     v                  v
PII Agent          Security Agent
     |                  |
     +---------+--------+
               |
               v
       Evaluation Agent
               |
          +----+----+
          |         |
        PASS       REVIEW
          |
          v
     MCP Tool Layer
          |
          v
 Fabric / Power BI Work
          |
          v
 Deterministic Reconciliation
          |
      +---+---+
      |       |
    PASS    REVIEW
```

The point of the design is **not** to create as many agents as possible. Reasoning tasks go to the model; guarantees stay in code.

## What can be automated in a real migration

A production implementation can extend the demo in these directions:

1. **Source Discovery:** automatically build a dependency graph from report metadata and data-source definitions.
2. **Transformation Mapping:** classify each legacy calculation as Fabric transformation, semantic-model measure, report filter, or human-review case.
3. **Report Similarity:** detect repeated business logic across reports and create reusable transformations or measures.
4. **Migration Planning:** score reports by dependencies, transformation count, complexity, and risk to create a migration queue.
5. **PII Classification:** scan fields and sample values, redact protected fields, and record why data was excluded from an AI call.
6. **Human Review Queue:** route low-confidence or security-sensitive mappings to an approval step and resume the workflow after a decision.
7. **Regression Evaluation:** run reconciliation and RAGAS checks automatically on prompt/model/retrieval changes.
8. **Cost Routing:** send simple interpretation jobs to smaller models and reserve higher-cost models for complex cases.
9. **MCP Tooling:** expose controlled actions such as `list_report_dependencies`, `get_transformation`, `validate_report`, and `submit_for_review` behind authorization.
10. **Performance Monitoring:** track P50/P95/P99 latency, token usage, cache hits, and model cost over time.

These are engineering extensions of the same core workflow; the public demo intentionally keeps the data synthetic and the external system integrations mocked or represented by small local interfaces.

## Run locally in VS Code

```bash
cd projects/ai-assisted-bi-migration/demo
python -m venv .venv

# Windows
.venv\\Scripts\\activate

pip install -r requirements.txt
python -m demo.app
```

The demo runs without Azure credentials using deterministic fallback logic. To enable Azure OpenAI mode, copy `.env.example` to `.env` and provide the endpoint, key, and deployment.

## Target architecture

```text
81 Legacy Spotfire Reports
            |
            v
    Discovery / Inventory
            |
      +-----+-----+
      |           |
      v           v
Deterministic   LLM-assisted
analysis        interpretation
      |           |
      +-----+-----+
            |
            v
      Migration Plan
            |
     Security + PII
            |
            v
      Human Review
            |
            v
   Fabric Transformations
            |
            v
      Curated Data
            |
            v
    Power BI Semantic Model
            |
            v
       Power BI Report
            |
            v
 Validation + Evaluation
            |
       +----+----+
       |         |
      PASS     REVIEW
```

## Core engineering principle

> **Use agents where the problem requires interpretation. Use deterministic services where the system needs guarantees.**

The project is deliberately closer to an engineering workflow than a generic multi-agent chatbot. The interesting part is how AI is placed inside an existing enterprise migration process without giving the model authority over permissions, correctness, or release decisions.

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
├── demo/
│   ├── __init__.py
│   ├── app.py
│   ├── agents.py
│   ├── models.py
│   ├── sample_report.json
│   ├── requirements.txt
│   └── .env.example
└── src/
    └── validate/
        └── reconciliation.py
```
