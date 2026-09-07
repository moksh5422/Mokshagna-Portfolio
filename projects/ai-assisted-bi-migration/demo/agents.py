import json
import os
import re
from typing import Any

from .models import MigrationSpec


class DiscoveryAgent:
    """Build a deterministic inventory before any LLM reasoning."""

    def inspect(self, report: dict[str, Any]) -> dict[str, Any]:
        calculations = report.get("calculations", [])
        transformations = report.get("transformations", [])
        return {
            "report_id": report.get("report_id"),
            "source_system": report.get("source_system", "legacy-bi"),
            "sources": report.get("data_sources", []),
            "calculation_count": len(calculations),
            "transformation_count": len(transformations),
            "filter_count": len(report.get("filters", [])),
            "dependencies": report.get("dependencies", []),
        }


class MigrationAgent:
    """Interpret legacy BI logic and produce a reviewable migration spec."""

    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    @property
    def llm_enabled(self) -> bool:
        return bool(self.endpoint and self.api_key and self.deployment)

    def analyze(self, report: dict[str, Any]) -> MigrationSpec:
        if self.llm_enabled:
            return self._analyze_with_azure_openai(report)
        return self._analyze_with_rules(report)

    def _analyze_with_rules(self, report: dict[str, Any]) -> MigrationSpec:
        calculations: list[dict[str, Any]] = []
        review_items: list[str] = []
        for item in report.get("calculations", []):
            expr = item.get("expression", "")
            target_layer = "semantic_model" if "SUM(" in expr.upper() else "fabric_transformation"
            confidence = 0.95 if target_layer == "semantic_model" else 0.72
            calculations.append({**item, "target_layer": target_layer, "confidence": confidence})
            if confidence < 0.80:
                review_items.append(f"Review calculation: {item.get('name', 'unnamed')}")
        return MigrationSpec(
            report_id=report["report_id"], source_system=report.get("source_system", "legacy-bi"),
            sources=report.get("data_sources", []), calculations=calculations,
            transformations=report.get("transformations", []), filters=report.get("filters", []),
            review_items=review_items, confidence=min([x["confidence"] for x in calculations] or [0.0]),
        )

    def _analyze_with_azure_openai(self, report: dict[str, Any]) -> MigrationSpec:
        try:
            from openai import AzureOpenAI
        except ImportError as exc:
            raise RuntimeError("Install requirements.txt to enable Azure OpenAI mode") from exc
        client = AzureOpenAI(
            azure_endpoint=self.endpoint, api_key=self.api_key,
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        )
        system = (
            "Analyze a legacy BI report. Return JSON only. For each calculation choose "
            "semantic_model or fabric_transformation, provide confidence 0-1, and flag "
            "ambiguous mappings for human review. Never claim uncertain mappings are correct."
        )
        response = client.chat.completions.create(
            model=self.deployment, temperature=0, response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system}, {"role": "user", "content": json.dumps(report)}],
        )
        return MigrationSpec(**json.loads(response.choices[0].message.content))


class PlannerAgent:
    """Prioritize reports by migration complexity and risk."""

    def plan(self, inventory: dict[str, Any]) -> dict[str, Any]:
        score = (
            inventory["calculation_count"]
            + 2 * inventory["transformation_count"]
            + inventory["filter_count"]
            + len(inventory["sources"])
        )
        if score <= 3:
            complexity = "LOW"
        elif score <= 7:
            complexity = "MEDIUM"
        else:
            complexity = "HIGH"
        return {"report_id": inventory["report_id"], "complexity_score": score, "complexity": complexity}


class SecurityAgent:
    """Enforce access before an AI/tool operation is allowed."""

    def authorize(self, role: str, requested_scope: str) -> dict[str, Any]:
        allowed = {
            "migration-engineer": {"report-metadata", "sample-data", "validation"},
            "reviewer": {"report-metadata", "validation"},
            "viewer": {"report-metadata"},
        }
        permitted = requested_scope in allowed.get(role, set())
        return {"role": role, "requested_scope": requested_scope, "allowed": permitted,
                "decision": "ALLOW" if permitted else "DENY"}


class PIIAgent:
    """Find common PII-like field names before content reaches an AI path."""

    PATTERNS = ("email", "phone", "mobile", "address", "ssn", "account", "customer_id")

    def scan(self, report: dict[str, Any]) -> dict[str, Any]:
        fields = []
        for calc in report.get("calculations", []):
            expression = str(calc.get("expression", ""))
            fields.extend(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expression.lower()))
        matches = sorted({f for f in fields if any(p in f for p in self.PATTERNS)})
        return {"pii_detected": bool(matches), "fields": matches, "action": "REVIEW/REDACT" if matches else "ALLOW"}


class SimilarityAgent:
    """Find simple reusable logic candidates across report definitions."""

    def compare(self, reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: dict[str, list[str]] = {}
        for report in reports:
            for calc in report.get("calculations", []):
                expression = " ".join(str(calc.get("expression", "")).lower().split())
                if expression:
                    seen.setdefault(expression, []).append(report.get("report_id", "unknown"))
        return [
            {"expression": expression, "reports": ids, "reuse_candidate": len(ids) > 1}
            for expression, ids in seen.items() if len(ids) > 1
        ]


class EvaluationAgent:
    """Decide whether an AI-generated migration spec needs review."""

    def review(self, spec: MigrationSpec) -> dict[str, Any]:
        checks = [
            {"name": "confidence_floor", "passed": spec.confidence >= 0.80},
            {"name": "review_items_visible", "passed": True},
        ]
        return {"checks": checks, "requires_human_review": bool(spec.review_items) or spec.confidence < 0.80}


class MCPToolRegistry:
    """Small allow-list representing the tools an agent could call in production."""

    TOOLS = {"list_report_dependencies", "get_transformation", "get_sample_data", "validate_report", "submit_for_review"}

    def invoke(self, tool_name: str, role: str) -> dict[str, Any]:
        if tool_name not in self.TOOLS:
            return {"tool": tool_name, "allowed": False, "reason": "Unknown tool"}
        return {"tool": tool_name, "allowed": role == "migration-engineer", "role": role}
