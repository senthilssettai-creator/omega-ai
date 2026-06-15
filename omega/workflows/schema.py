from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class WorkflowStepSchema:
    name: str
    action: str
    parameters: dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowSchema:
    name: str
    description: str
    steps: list[WorkflowStepSchema] = field(default_factory=list)
