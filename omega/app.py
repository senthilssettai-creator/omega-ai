from fastapi import FastAPI
from .config import Settings
from .agents.manager import AgentManager
from .memory.manager import MemoryManager


def create_api_app(settings: Settings) -> FastAPI:
    app = FastAPI(title="OMEGA Agent API")
    agent_manager = AgentManager(settings=settings)
    memory_manager = MemoryManager(settings=settings)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.post("/goals")
    async def submit_goal(goal: dict):
        result = agent_manager.submit_goal(goal["text"])
        return {"result": result}

    @app.get("/status")
    async def get_status():
        return {"status": agent_manager.status()}

    @app.get("/memory")
    async def query_memory(q: str):
        return {"results": memory_manager.search(q)}

    @app.get("/workflows")
    async def list_workflows():
        return {"workflows": agent_manager.workflow_manager.list_workflows()}

    @app.post("/workflows/{name}/execute")
    async def execute_workflow(name: str):
        return {"results": agent_manager.run_workflow(name)}

    return app
