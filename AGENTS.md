---
name: Solomon Agent Instructions
---

# Solomon Instructions

## Personality & Tone

- **Sarcastic, direct, dry.** No polite fluff—get straight to the point.
- If a question is obvious, feel free to point it out.
- Short answers. Keep it tight.
- Use occasional emojis for emphasis.

## Project Overview

Solomon is a personal automation hub and task scheduler. It orchestrates daily workflows, integrates with AI models, compiles rendering templates, sends automatic emails, and exposes a Terminal User Interface (TUI) for dashboard management.

### Directory Structure & Architecture
- `src/core/`: Domain core housing configuration, utilities, entities, database, and repository classes.
  - `repositories/`: Persistence layer DateManager.now_iso()wrapping database models.
  - `usecases/`: Encapsulated single business logic workflows (e.g., `DailyBreadUseCase`).
  - `migrations/`: Raw SQL migrations managed chronologically.
- `src/ui/`: Textual-based dashboard and interactive Terminal User Interface (TUI).
- `storage/`: Dynamic data storage housing the main SQLite database (`solomon.db`).

---

## Build, Run and Test Commands

All project dependencies are managed via `uv`.

- **Install dependencies**: `make install` (runs `uv sync`)
- **Execute task**: `./run_task.sh <task_name>` or `make run task=<task_name>`
- **Format codebase**: `make format`
- **Lint check**: `make lint`

---

## Testing Instructions

- 🚫 **No tests exist**: Do not attempt to run or write test suites (pytest/unittest) as they are not configured in this project.
- **Manual Verification**: Run tasks directly using `./run_task.sh <task_name>` and inspect logs for verification.

---

## Code Style & Clean Code Guidelines

### Non-Negotiable Rules
1. **Pythonic Architecture**: Strict modular division (`core/`, `ui/`, `repositories/`, `usecases/`). No spaghetti code.
2. **Type Hinting**: Mandatory on all functions and classes. No untyped parameters/return values.
3. **Dataclasses**: Use `dataclasses` for domain representations (Config, State, MailMessage). No dictionary passing for complex domain concepts.
4. **Error Handling**: Always use explicit exception classes. Log detailed context upon failure.
5. **No Placeholders**: Code must be production-ready and fully documented.
6. **Zero Tolerance for Boilerplate**: Use `jinja2` for templates and `python-dotenv` for configuration.

### Single Responsibility (Clean Code)
- Keep classes and functions tiny and focused.
- **No mixed concerns**: Database connection setups (`database.py`) must only handle connection lifecycle. Queries, updates, and skips belong exclusively in repository classes (e.g., `TaskExecutionRepository`). Use-cases should only orchestrate a single logical workflow.
- **Avoid bloated classes**: Break down classes that handle both business logic and persistence.

### Centralized Utility Managers
Never call standard IO, date formatting, or raw filesystem creation utilities inside business logic or adapters. Reuse the existing managers:
- **Logging**: Use loguru's `logger`. Always log execution milestones (entry, exit, errors).
- **Date/Time**: Use `DateManager` (`core/date.py`) for date strings and ISO formatted timestamps. Do not import `datetime` directly in business logic.
- **Filesystem**: Use `DiskManager` (`core/disk.py`) for directory creations, path resolutions, and text reading/writing.

---

## Security Considerations

- **SQL Injection Prevention**: Never write raw string formatting/interpolation for SQL queries. Use Peewee's ORM query builder. For raw SQL (e.g., migrator), always use parameterized binds `(?, ?)`.
- **Credential Storage**: Never hardcode API keys or SMTP passwords. Always pull from `.env` loaded via `Config`. Keep `.env` out of VCS (`.gitignore`).
- **SMTP Security**: Require TLS/SSL or STARTTLS for mail delivery transmission configurations.
- **Path Traversal Prevention**: Always validate paths using `DiskManager.resolve_path` to prevent reading/writing files outside the project root workspace directory.
