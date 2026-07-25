-- Remove auth-related tables
DROP TABLE IF EXISTS blacklisted_tokens;
DROP TABLE IF EXISTS magic_codes;

-- Remove user_id FK from conversations (SQLite: recreate table)
CREATE TABLE IF NOT EXISTS conversations_new (
    id TEXT PRIMARY KEY,
    title TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

INSERT INTO conversations_new (id, title, created_at, updated_at)
SELECT id, title, created_at, updated_at FROM conversations;

DROP TABLE conversations;
ALTER TABLE conversations_new RENAME TO conversations;

-- Remove users table
DROP TABLE IF EXISTS users;
