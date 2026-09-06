# Version 2 — Secure the AI Workflow

Once the workflow could inspect and interpret enterprise report metadata, the next problem was access control.

The design keeps security outside the model. The application decides what an identity is allowed to read or do before an AI request is made.

## Controls

- RBAC and identity-based access
- PII detection and redaction
- Controlled access to source data
- Secret management
- Guardrails around model inputs and outputs
- Audit-friendly request paths

## Design principle

```text
User / Service Identity
        |
        v
   Authorization
        |
   +----+----+
   |         |
 Allowed   Denied
   |
   v
AI / Tool Request
```

The model can propose an action, but it does not receive permissions simply because it requested them.

## Goal

Make AI-assisted migration useful with enterprise information without making the LLM the security boundary.
