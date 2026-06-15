from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import json

WORKFLOW_STORE = Path("./omega_workflows.json")

@dataclass
class WorkflowStep:
    name: str
    action: str
    parameters: dict[str, Any] = field(default_factory=dict)

@dataclass
class Workflow:
    name: str
    description: str
    steps: list[WorkflowStep] = field(default_factory=list)

class WorkflowManager:
    def __init__(self, store_path: Path | str = WORKFLOW_STORE):
        self.store_path = Path(store_path).expanduser().resolve()
        self.workflows: dict[str, Workflow] = {}
        self.load_workflows()

    def load_workflows(self) -> None:
        if self.store_path.exists():
            with self.store_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            for name, payload in data.items():
                self.workflows[name] = Workflow(
                    name=name,
                    description=payload["description"],
                    steps=[WorkflowStep(**step) for step in payload["steps"]],
                )

    def save_workflows(self) -> None:
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            name: {
                "description": workflow.description,
                "steps": [step.__dict__ for step in workflow.steps],
            }
            for name, workflow in self.workflows.items()
        }
        with self.store_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def create_workflow(self, name: str, description: str, steps: list[WorkflowStep]) -> Workflow:
        workflow = Workflow(name=name, description=description, steps=steps)
        self.workflows[name] = workflow
        self.save_workflows()
        return workflow

    def list_workflows(self) -> list[str]:
        return list(self.workflows.keys())

    def get_workflow(self, name: str) -> Workflow | None:
        return self.workflows.get(name)
