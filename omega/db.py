from pathlib import Path

import duckdb

class DuckDBStore:
    def __init__(self, database_path: str = "./omega.duckdb"):
        self.path = Path(database_path).expanduser().resolve()
        self.conn = duckdb.connect(str(self.path))

    def initialize(self) -> None:
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS omega_event_seq START 1")
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS event_log (
                id BIGINT PRIMARY KEY DEFAULT nextval('omega_event_seq'),
                timestamp TIMESTAMP DEFAULT current_timestamp,
                category TEXT,
                action TEXT,
                outcome TEXT
            )
            """
        )

    def log_event(self, category: str, action: str, outcome: str) -> None:
        self.conn.execute(
            "INSERT INTO event_log (category, action, outcome) VALUES (?, ?, ?)",
            (category, action, outcome),
        )

    def recent_events(self, limit: int = 20) -> list[tuple]:
        result = self.conn.execute(
            "SELECT timestamp, category, action, outcome FROM event_log ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        )
        return result.fetchall()