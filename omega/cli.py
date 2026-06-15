import os
from typing import Optional
import typer
from .app import create_api_app
from .agents.manager import AgentManager
from .memory.manager import MemoryManager
from .config import Settings

app = typer.Typer(help="OMEGA autonomous AI agent CLI")

settings = Settings()
agent_manager = AgentManager(settings=settings)
memory_manager = MemoryManager(settings=settings)

@app.command()
def run(host: str = "127.0.0.1", port: int = 8080):
    """Run the Omega API server."""
    import uvicorn

    app = create_api_app(settings)
    uvicorn.run(app, host=host, port=port)

@app.command()
def goal(text: str):
    """Submit a goal for Omega to execute."""
    result = agent_manager.submit_goal(text)
    typer.echo(result)

@app.command()
def workflows():
    """List configured workflows."""
    names = agent_manager.workflow_manager.list_workflows()
    typer.echo("\n".join(names or ["No workflows configured."]))

@app.command()
def run_workflow(name: str):
    """Execute a named workflow."""
    results = agent_manager.run_workflow(name)
    typer.echo("\n".join(results))

@app.command()
def dashboard():
    """Open a live Omega progress dashboard."""
    from .ui import OmegaDashboard

    dashboard = OmegaDashboard()
    try:
        dashboard.run(lambda: agent_manager.live_log)
    except KeyboardInterrupt:
        typer.echo("Dashboard closed.")

@app.command()
def status():
    """Show current agent status."""
    status = agent_manager.status()
    typer.echo(status)

@app.command()
def memory(query: str):
    """Search Omega long-term memory."""
    items = memory_manager.search(query)
    typer.echo("\n".join(items or ["No entries found."]))

def main():
    app()
