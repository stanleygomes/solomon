CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS magic_codes (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    code TEXT NOT NULL,
    attempts INTEGER DEFAULT 0,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS blacklisted_tokens (
    token TEXT PRIMARY KEY,
    blacklisted_at TEXT NOT NULL,
    expires_at TEXT NOT NULL
);
