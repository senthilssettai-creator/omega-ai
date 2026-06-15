from time import sleep
from typing import List

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

console = Console()

class OmegaDashboard:
    def __init__(self):
        self.lines: List[str] = []

    def update(self, lines: List[str]) -> None:
        self.lines = lines[-20:]

    def render(self) -> Panel:
        table = Table.grid(expand=True)
        table.add_column("Event", ratio=1)
        for line in self.lines:
            table.add_row(line)
        return Panel(table, title="OMEGA Live Progress", border_style="bright_blue")

    def run(self, get_lines_callable, refresh: float = 0.5) -> None:
        with Live(self.render(), refresh_per_second=2, console=console):
            while True:
                lines = get_lines_callable()
                self.update(lines)
                sleep(refresh)
