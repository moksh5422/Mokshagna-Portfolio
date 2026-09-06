# LinkedIn Post

I didn’t approach 81 report migrations as a BI migration problem.

I approached it as a software engineering problem.

We had 81 Spotfire reports backed by multiple data sources, legacy transformations, calculated logic, filters, and business rules.

The obvious approach was:

**Open report -> understand it -> rebuild it in Power BI -> test it -> repeat.**

That approach does not scale well.

The difficult part was not creating the Power BI visuals.

The difficult part was figuring out:

**What does this report actually depend on?**

**Where is this calculation happening?**

**Which logic belongs in Fabric and which belongs in the semantic model?**

**How do we know the migrated report is actually equivalent to the old one?**

So I started treating the migration as a repeatable engineering workflow rather than a collection of dashboards.

I built the process around five things:

-> **Inventory:** understand the report, source, calculations, filters and dependencies before development starts.

-> **Transformation mapping:** trace legacy transformations and decide where they should live in the new Fabric architecture rather than blindly reproducing them inside Power BI.

-> **AI-assisted analysis:** use an LLM to help interpret legacy expressions, suggest equivalent transformations and flag ambiguous logic.

The model was not allowed to make the final decision.

It produced a proposed mapping, and uncertain cases were sent for review.

-> **Validation:** compare the old and new systems using record counts, aggregates, filters, measures and other business-level checks instead of relying on “the dashboard looks right.”

-> **Exception handling:** automate the predictable cases and focus human attention on the reports where dependencies, transformations or results do not reconcile cleanly.

That changed the problem from:

**81 individual migrations**

to:

**one migration system with 81 inputs.**

The important lesson for me was that AI was not the solution by itself.

The useful part was combining:

**AI + data engineering + validation + security + human review + production constraints.**

That is how I increasingly think about Forward Deployed Engineering.

The job is not:

> “Here is an LLM. What can we build with it?”

It is:

> “Here is a messy business problem. Where can software, data, and AI actually remove the bottleneck?”

I’ve documented a sanitized version of the approach on GitHub, using synthetic examples rather than any client data.

#AIEngineering #ForwardDeployedEngineering #DataEngineering #MicrosoftFabric #PowerBI #GenAI #EnterpriseAI
