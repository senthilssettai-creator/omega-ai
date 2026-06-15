from typing import List

from .planner import PlannerAgent
from .research import ResearchAgent
from .coding import CodingAgent
from .browser import BrowserAgent
from .devops import DevOpsAgent
from .memory import MemoryAgent
from .critic import CriticAgent
from .executor import ExecutorAgent
from ..config import Settings
from ..db import DuckDBStore
from ..memory.manager import MemoryManager
from ..mcp.manager import MCPManager
from ..openrouter_client import OpenRouterClient
from ..plugins.manager import PluginManager
from ..workflows.manager import WorkflowManager
from ..workflows.engine import WorkflowEngine

class AgentManager:
    def __init__(self, settings: Settings, workflow_manager: WorkflowManager | None = None):
        self.settings = settings
        self.openrouter = OpenRouterClient(settings=settings)
        self.planner = PlannerAgent(settings=settings, client=self.openrouter)
        self.research = ResearchAgent(settings=settings, client=self.openrouter)
        self.coding = CodingAgent(settings=settings, client=self.openrouter)
        self.browser = BrowserAgent(settings=settings)
        self.devops = DevOpsAgent(settings=settings)
        self.memory = MemoryAgent(settings=settings)
        self.critic = CriticAgent(settings=settings)
        self.executor = ExecutorAgent(settings=settings, client=self.openrouter)
        self.plugin_manager = PluginManager()
        self.mcp_manager = MCPManager(settings=settings)
        self.memory_manager = MemoryManager(settings=settings)
        self.workflow_manager = workflow_manager or WorkflowManager()
        self.workflow_engine = WorkflowEngine(agent_manager=self)
        self.event_store = DuckDBStore()
        self.event_store.initialize()
        self.task_log: List[str] = []
        self.live_log: List[str] = []

    def submit_goal(self, goal: str) -> str:
        self.task_log.append(goal)
        self.memory_manager.store("goal", goal)
        self.event_store.log_event("goal", goal, "submitted")
        self.report_progress(f"Goal received: {goal}")
        plan = self.planner.create_plan(goal)
        self.report_progress("Plan created")
        execution = self.workflow_engine.execute_plan(plan)
        self.event_store.log_event("execution", plan, "; ".join(execution)[:240])
        self.report_progress("Plan execution completed")
        return "\n".join(execution)

    def run_workflow(self, name: str) -> list[str]:
        workflow = self.workflow_manager.get_workflow(name)
        if not workflow:
            return [f"Workflow '{name}' not found."]
        self.event_store.log_event("workflow", name, "started")
        self.report_progress(f"Workflow started: {name}")
        results = self.workflow_engine.execute_workflow(workflow)
        self.event_store.log_event("workflow", name, "completed")
        self.report_progress(f"Workflow completed: {name}")
        return results

    def report_progress(self, message: str) -> None:
        self.live_log.insert(0, message)
        self.live_log = self.live_log[:50]

    def status(self) -> str:
        return f"Omega is ready. Last goal: {self.task_log[-1] if self.task_log else 'none'}"

    def list_plugins(self) -> List[str]:
        return self.plugin_manager.list_plugins()

    def list_mcp_servers(self) -> List[str]:
        entries = self.mcp_manager.list_servers()
        return [f"{name}: {url}" for name, url in entries.items()]
