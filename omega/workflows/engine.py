from __future__ import annotations
import re
from typing import TYPE_CHECKING, List

from .manager import Workflow, WorkflowStep

if TYPE_CHECKING:
    from ..agents.manager import AgentManager

class WorkflowEngine:
    def __init__(self, agent_manager: "AgentManager"):
        self.agent_manager = agent_manager

    def execute_workflow(self, workflow: Workflow) -> List[str]:
        results: List[str] = []
        for step in workflow.steps:
            self.agent_manager.report_progress(f"Executing workflow step: {step.name} ({step.action})")
            result = self._dispatch(step)
            self.agent_manager.report_progress(f"Step completed: {step.name} -> {result[:120]}")
            results.append(f"{step.name}: {result}")
        return results

    def execute_plan(self, plan: str) -> List[str]:
        steps = [line.strip() for line in plan.splitlines() if line.strip()]
        results: List[str] = []
        for line in steps:
            self.agent_manager.report_progress(f"Executing plan step: {line}")
            if "research" in line.lower():
                result = self.agent_manager.research.investigate(line)
            elif "code" in line.lower() or "implement" in line.lower():
                result = self.agent_manager.coding.develop(line)
            elif "visit" in line.lower() or "navigate" in line.lower():
                target = self._extract_url(line)
                result = self.agent_manager.browser.visit(target)
            else:
                result = self.agent_manager.executor.execute(line)
            self.agent_manager.memory_manager.store("workflow", f"{line} -> {result}")
            self.agent_manager.report_progress(f"Plan step completed: {line} -> {result[:120]}")
            results.append(result)
        return results

    def _dispatch(self, step: WorkflowStep) -> str:
        action = step.action.lower()
        params = step.parameters or {}

        if action == "visit":
            return self.agent_manager.browser.visit(params.get("url", ""))
        if action == "fill_form":
            return self.agent_manager.browser.fill_form(
                params.get("url", ""),
                params.get("fields", {}),
                params.get("submit_selector"),
            )
        if action == "extract_text":
            return self.agent_manager.browser.extract_text(
                params.get("url", ""),
                params.get("selector", ""),
            )
        if action == "research":
            return self.agent_manager.research.investigate(params.get("query", ""))
        if action == "search_web":
            return self.agent_manager.research.search_web(params.get("url", ""))
        if action == "code":
            return self.agent_manager.coding.develop(params.get("task", ""))
        if action == "review_code":
            return self.agent_manager.coding.review(params.get("code", ""))
        if action == "generate_tests":
            return self.agent_manager.coding.generate_tests(params.get("description", ""))
        if action == "plan":
            return self.agent_manager.planner.create_plan(params.get("goal", ""))
        if action == "git_status":
            return self.agent_manager.devops.git_status()
        if action == "git_commit":
            return self.agent_manager.devops.git_commit(params.get("message", "Commit from Omega"))
        if action == "docker_build":
            return self.agent_manager.devops.docker_build(params.get("tag", "omega-ai"), params.get("dockerfile", "Dockerfile"))
        if action == "shell":
            return self.agent_manager.devops.shell(params.get("command", ""))
        if action == "store_memory":
            self.agent_manager.memory_manager.store(params.get("category", "general"), params.get("content", ""))
            return "Memory stored"
        if action == "recall_memory":
            results = self.agent_manager.memory_manager.search(params.get("query", ""))
            return "; ".join(results)

        return self.agent_manager.executor.execute(step.name)

    def _extract_url(self, text: str) -> str:
        match = re.search(r"https?://[\w\-./?=&%]+", text)
        return match.group(0) if match else "http://example.com"
