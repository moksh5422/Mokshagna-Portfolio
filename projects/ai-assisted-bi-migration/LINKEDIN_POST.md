# LinkedIn Post

I was working on an 81-report Spotfire to Power BI/Fabric migration.

At first, it looked like a reporting problem.

It turned out to be a much narrower engineering problem:

**How do you use AI to understand legacy BI logic without making the AI responsible for security, correctness, or production performance?**

I worked through it in three versions.

### V1 — Understand the legacy logic

The first bottleneck was discovery.

Reports had different sources, transformations, calculations, filters, and business rules. Rebuilding them one by one meant repeating the same investigation.

I used an LLM to help interpret legacy expressions, suggest target transformations, group similar logic, and flag cases that looked ambiguous.

The model produced a proposed mapping. It did not decide that the mapping was correct.

### V2 — Put security outside the model

Once AI was working with enterprise information, the next problem was access.

I added **RBAC, identity-based access, PII handling, and controlled data access** so that permissions were enforced by the application instead of being left to the model.

That distinction mattered:

**the model can request an operation; the application decides whether it is allowed.**

### V3 — Prove it and make it usable

Then came two production questions:

**Is the AI actually helping?**

**Is the system fast enough to use?**

I used **RAGAS** to evaluate retrieval and answer quality as prompts, chunking, models, and search settings changed.

For the migration itself, deterministic checks compared things like row counts, aggregates, measures, and filters between the old and new systems.

I also worked on latency across retrieval, context construction, model calls, caching, and response delivery, including **SSE streaming**. The workload saw roughly **250 ms improvement at P95**.

The result was a different way of thinking about the migration.

Not:

**81 reports to rebuild.**

But:

**one repeatable system that can analyse 81 reports, protect the data it touches, measure whether its AI output is useful, and surface the cases that still need an engineer.**

That is the part of Forward Deployed Engineering I find interesting.

The hard problem usually isn't “how do I add an LLM?”

It is:

> **Where can AI remove a real bottleneck inside an existing system without creating a bigger problem somewhere else?**

I’ve put a sanitized version of the approach on GitHub using synthetic examples only.

#AIEngineering #ForwardDeployedEngineering #EnterpriseAI #RAG #MicrosoftFabric #PowerBI #DataEngineering
