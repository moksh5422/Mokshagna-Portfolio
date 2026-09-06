from dataclasses import dataclass, field
from typing import Any


@dataclass
class MigrationSpec:
    report_id: str
    source_system: str
    sources: list[str]
    calculations: list[dict[str, Any]]
    transformations: list[dict[str, Any]]
    filters: list[dict[str, Any]]
    review_items: list[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class DemoResult:
    report_id: str
    inventory: dict[str, Any]
    migration_spec: MigrationSpec
    security: dict[str, Any]
    validation: list[dict[str, Any]]
    route: str
    notes: list[str]
