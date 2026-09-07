import json
from pathlib import Path

from dotenv import load_dotenv

from .agents import (
    DiscoveryAgent,
    EvaluationAgent,
    MCPToolRegistry,
    MigrationAgent,
    PIIAgent,
    PlannerAgent,
    SecurityAgent,
    SimilarityAgent,
)

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")


def reconcile(source: dict, target: dict) -> list[dict]:
    checks = []
    for key in ("row_count", "revenue"):
        source_value = source.get(key)
        target_value = target.get(key)
        checks.append({
            "name": key,
            "source": source_value,
            "target": target_value,
            "status": "PASS" if source_value == target_value else "REVIEW",
        })
    return checks


def run_report(report: dict) -> dict:
    discovery = DiscoveryAgent()
    planner = PlannerAgent()
    pii = PIIAgent()
    migration = MigrationAgent()
    security = SecurityAgent()
    evaluation = EvaluationAgent()
    tools = MCPToolRegistry()

    inventory = discovery.inspect(report)
    plan = planner.plan(inventory)
    pii_result = pii.scan(report)
    spec = migration.analyze(report)
    security_result = security.authorize("migration-engineer", "sample-data")
    eval_result = evaluation.review(spec)
    tool_result = tools.invoke("get_transformation", "migration-engineer")
    checks = reconcile({"row_count": 100000, "revenue": 1250000}, {"row_count": 100000, "revenue": 1249997})

    return {
        "inventory": inventory,
        "plan": plan,
        "pii": pii_result,
        "migration_spec": spec.__dict__,
        "security": security_result,
        "evaluation": eval_result,
        "tool": tool_result,
        "reconciliation": checks,
    }


def main() -> None:
    report_path = ROOT / "sample_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    print("=== LEGACY BI MIGRATION DEMO ===")
    print("AI analysis mode:", "Azure OpenAI" if MigrationAgent().llm_enabled else "local deterministic fallback")

    result = run_report(report)
    print(json.dumps(result, indent=2))

    print("\n=== SIMILARITY / REUSE CHECK ===")
    similar = SimilarityAgent().compare([report, report | {"report_id": "sales-overview-copy"}])
    print(json.dumps(similar, indent=2))

    needs_review = (
        result["evaluation"]["requires_human_review"]
        or result["pii"]["pii_detected"]
        or any(c["status"] == "REVIEW" for c in result["reconciliation"])
    )
    print("\n=== DECISION ===")
    print("HUMAN REVIEW REQUIRED" if needs_review else "READY FOR MIGRATION")


if __name__ == "__main__":
    main()
