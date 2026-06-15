import os
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from omega.agents.manager import AgentManager
from omega.config import Settings
from omega.db import DuckDBStore
from omega.workflows.manager import WorkflowManager, WorkflowStep


class DummySettings(Settings):
    openrouter_api_key: str | None = None
    playwright_headless: bool = True


def test_workflow_execution_reports_progress(tmp_path: Path):
    workflow_store = tmp_path / "omega_workflows.json"
    workflow_manager = WorkflowManager(store_path=workflow_store)
    workflow_manager.create_workflow(
        name="test-workflow",
        description="A workflow that runs a shell command",
        steps=[
            WorkflowStep(name="Check repo", action="git_status", parameters={}),
            WorkflowStep(name="List files", action="shell", parameters={"command": "echo hello"}),
        ],
    )

    db_path = tmp_path / "omega.duckdb"
    agent_manager = AgentManager(
        settings=DummySettings(),
        workflow_manager=workflow_manager,
    )
    agent_manager.event_store = DuckDBStore(str(db_path))
    agent_manager.event_store.initialize()

    results = agent_manager.run_workflow("test-workflow")

    assert any("Workflow started" in line for line in agent_manager.live_log)
    assert any("Workflow completed" in line for line in agent_manager.live_log)
    assert any("Executing workflow step: Check repo" in line for line in agent_manager.live_log)
    assert any("Executing workflow step: List files" in line for line in agent_manager.live_log)
    assert len(results) == 2
    assert results[0].startswith("Check repo:")
    assert results[1].startswith("List files:")


def test_workflow_store_isolated(tmp_path: Path):
    workflow_store = tmp_path / "omega_workflows.json"
    workflow_manager = WorkflowManager(store_path=workflow_store)
    workflow_manager.create_workflow(
        name="isolated-workflow",
        description="Isolated workflow test",
        steps=[WorkflowStep(name="Step", action="shell", parameters={"command": "echo isolated"})],
    )

    loaded = WorkflowManager(store_path=workflow_store).get_workflow("isolated-workflow")
    assert loaded is not None
    assert loaded.name == "isolated-workflow"
