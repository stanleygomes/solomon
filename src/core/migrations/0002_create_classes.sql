CREATE TABLE IF NOT EXISTS classes (
    id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,
    duration_days INTEGER NOT NULL,
    current_day INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);
