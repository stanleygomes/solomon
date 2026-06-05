CREATE TABLE IF NOT EXISTS lessons (
    id TEXT PRIMARY KEY,
    class_id TEXT NOT NULL,
    day_number INTEGER NOT NULL,
    topic TEXT NOT NULL,
    summary TEXT,
    status TEXT NOT NULL,
    FOREIGN KEY(class_id) REFERENCES classes(id) ON DELETE CASCADE
);
