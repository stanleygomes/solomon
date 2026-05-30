CREATE TABLE IF NOT EXISTS task_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    status TEXT NOT NULL,
    executed_at TEXT NOT NULL
);
