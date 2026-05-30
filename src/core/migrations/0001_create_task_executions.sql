CREATE TABLE IF NOT EXISTS task_executions (
    id TEXT PRIMARY KEY,
    task_name TEXT NOT NULL,
    status TEXT NOT NULL,
    executed_at TEXT NOT NULL
);
