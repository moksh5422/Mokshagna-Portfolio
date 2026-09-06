import json
from pathlib import Path

from .agents import EvaluationAgent, MigrationAgent, SecurityAgent


ROOT = Path(__file__).resolve().parent


def reconcile(source: dict, target: dict) -> list[dict]:
    checks = []
    for key in ("row_count", "revenue"):
        source_value = source.get(key)
        target_value = target.get(key)
        checks.append(
            {
                "name": key,
                "source": source_value,
                "target": target_value,
                "status": "PASS" if source_value == target_value else "REVIEW",
            }
        )
    return checks


def main() -> None:
    report_path = ROOT / "sample_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))

    migration_agent = MigrationAgent()
    security_agent = SecurityAgent()
    evaluation_agent = EvaluationAgent()

    print("=== 1. MIGRATION ANALYSIS AGENT ===")
    spec = migration_agent.analyze(report)
    print(json.dumps(spec.__dict__, indent=2))

    print("\n=== 2. SECURITY AGENT ===")
    security = security_agent.authorize("migration-engineer", "sample-data")
    denied = security_agent.authorize("viewer", "sample-data")
    print("Allowed request:", json.dumps(security, indent=2))
    print("Denied request:", json.dumps(denied, indent=2))

    print("\n=== 3. EVALUATION AGENT ===")
    evaluation = evaluation_agent.review(spec)
    print(json.dumps(evaluation, indent=2))

    print("\n=== 4. DETERMINISTIC RECONCILIATION ===")
    checks = reconcile(
        {"row_count": 100000, "revenue": 1250000},
        {"row_count": 100000, "revenue": 1249997},
    )
    print(json.dumps(checks, indent=2))

    print("\n=== DECISION ===")
    needs_review = evaluation["requires_human_review"] or any(
        c["status"] == "REVIEW" for c in checks
    )
    print("HUMAN REVIEW REQUIRED" if needs_review else "READY FOR MIGRATION")


if __name__ == "__main__":
    main()
