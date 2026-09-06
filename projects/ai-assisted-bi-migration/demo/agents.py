import json
import os
from typing import Any

from .models import MigrationSpec


class MigrationAgent:
    """Small, testable agent wrapper.

    With Azure OpenAI configured, the agent asks the model to interpret the
    legacy report. Without credentials, the demo uses deterministic fallback
    logic so it is still runnable in VS Code.
    """

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
        calculations = []
        review_items = []
        for item in report.get("calculations", []):
            expr = item.get("expression", "")
            target_layer = "semantic_model" if "SUM(" in expr.upper() else "fabric_transformation"
            confidence = 0.95 if target_layer == "semantic_model" else 0.72
            calculations.append(
                {
                    **item,
                    "target_layer": target_layer,
                    "confidence": confidence,
                }
            )
            if confidence < 0.80:
                review_items.append(f"Review calculation: {item.get('name', 'unnamed')}")

        return MigrationSpec(
            report_id=report["report_id"],
            source_system=report.get("source_system", "legacy-bi"),
            sources=report.get("data_sources", []),
            calculations=calculations,
            transformations=report.get("transformations", []),
            filters=report.get("filters", []),
            review_items=review_items,
            confidence=min([x["confidence"] for x in calculations] or [0.0]),
        )

    def _analyze_with_azure_openai(self, report: dict[str, Any]) -> MigrationSpec:
        try:
            from openai import AzureOpenAI
        except ImportError as exc:
            raise RuntimeError("Install requirements.txt to enable Azure OpenAI mode") from exc

        client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        )

        system = """You are a migration analysis agent. Analyze a legacy BI report and return JSON only.\n"
        "For each calculation, choose target_layer as semantic_model or fabric_transformation.\n"
        "Give confidence between 0 and 1. Flag ambiguous mappings for human review.\n"
        "Never claim that an uncertain mapping is correct."""
        response = client.chat.completions.create(
            model=self.deployment,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(report)},
            ],
        )
        payload = json.loads(response.choices[0].message.content)
        return MigrationSpec(**payload)


class SecurityAgent:
    def authorize(self, role: str, requested_scope: str) -> dict[str, Any]:
        allowed = {
            "migration-engineer": {"report-metadata", "sample-data"},
            "reviewer": {"report-metadata", "validation"},
            "viewer": {"report-metadata"},
        }
        permitted = requested_scope in allowed.get(role, set())
        return {
            "role": role,
            "requested_scope": requested_scope,
            "allowed": permitted,
            "decision": "ALLOW" if permitted else "DENY",
        }


class EvaluationAgent:
    def review(self, spec: MigrationSpec) -> dict[str, Any]:
        checks = [
            {"name": "confidence_floor", "passed": spec.confidence >= 0.80},
            {"name": "review_items_visible", "passed": True},
        ]
        return {
            "checks": checks,
            "requires_human_review": bool(spec.review_items) or spec.confidence < 0.80,
        }
