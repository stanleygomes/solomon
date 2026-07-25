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

Solomon is a personal automation hub and task scheduler. It orchestrates daily workflows, integrates with AI models, compiles rendering templates, sends automatic emails, and exposes a CLI for command-line execution and a background cron daemon. It operates as a single-tenant application without authentication.

### Directory Structure & Architecture

```
src/
├── cli/                  # Typer & InquirerPy CLI interface
│   ├── commands/         # Individual command implementations (chat.py, update.py)
│   └── main.py           # CLI entrypoint
├── cron/                 # Background cron daemon (APScheduler)
│   └── jobs/             # Scheduled job definitions (e.g., daily_bread.py)
└── core/                 # Shared domain core
    ├── config/           # Environment loading (environment.py, logger.py)
    ├── constants/        # Project-wide constants
    ├── database/         # DB setup, models, repositories, migrations, seeders, DTOs
    │   ├── dto/
    │   ├── migrations/
    │   ├── models/
    │   ├── repositories/ # Persistence layer wrapping ORM models
    │   └── seeders/
    ├── exceptions/       # Custom exception classes
    ├── modules/          # Domain feature modules (e.g., daily_bread/, classes/)
    ├── services/         # External integrations (ai/, mail/, render/)
    ├── utils/            # Utility managers (date.py, disk.py, env.py, etc.)
    ├── workflow/         # Workflow orchestrator (orchestrator.py, base.py, dto.py)
    └── container.py      # Dependency container / service locator

storage/                  # SQLite database and dynamic data (solomon.db)
```

---

## Build, Run and Test Commands

All project dependencies are managed via `uv`.

| Command        | Description                              |
|----------------|------------------------------------------|
| `make install` | Setup project and install dependencies   |
| `make cli`     | Start interactive CLI                    |
| `make cron`    | Start background cron daemon (foreground)|
| `make seed`    | Populate database with initial seeds     |
| `make lint`    | Run linter (ruff) to check for issues    |
| `make format`  | Run formatter (ruff) to fix style        |
| `make clean`   | Remove cache, venv and temporary files   |

---

## Testing Instructions

- 🚫 **No tests exist**: Do not attempt to run or write test suites (pytest/unittest) as they are not configured in this project.
- **Manual Verification**: Run the relevant entrypoint (`make cron`, `make cli`) and inspect logs for verification.

---

## Code Style & Clean Code Guidelines

### Non-Negotiable Rules
1. **Pythonic Architecture**: Strict modular division (`cli/`, `cron/`, `core/`). No spaghetti code.
2. **Type Hinting**: Mandatory on all functions and classes. No untyped parameters/return values.
3. **Dataclasses**: Use `dataclasses` for domain representations (Config, State, MailMessage). No dictionary passing for complex domain concepts.
4. **Error Handling**: Always use explicit exception classes. Log detailed context upon failure.
5. **No Placeholders**: Code must be production-ready and fully documented.
6. **Zero Tolerance for Boilerplate**: Use `jinja2` for templates and `python-dotenv` for configuration.

### Single Responsibility (Clean Code)
- Keep classes and functions tiny and focused.
- **No mixed concerns**: DB setup (`database/setup.py`) handles only connection lifecycle. Queries belong exclusively in repository classes (`database/repositories/`). Workflows orchestrate a single logical flow.
- **Avoid bloated classes**: Break down classes that handle both business logic and persistence.
- **Layer boundaries**: `cli/` and `cron/` must only call `core/` — never each other. `core/` must not import from `cli/` or `cron/`.

### Centralized Utility Managers
Never call standard IO, date formatting, or raw filesystem utilities inside business logic or adapters. Reuse the existing managers in `core/utils/`:
- **Logging**: Use loguru's `logger`. Always log execution milestones (entry, exit, errors).
- **Date/Time**: Use `DateManager` (`core/utils/date.py`) for date strings and ISO formatted timestamps. Do not import `datetime` directly in business logic.
- **Filesystem**: Use `DiskManager` (`core/utils/disk.py`) for directory creation, path resolution, and text reading/writing.

---

## Security Considerations

- **SQL Injection Prevention**: Never write raw string formatting/interpolation for SQL queries. Use Peewee's ORM query builder. For raw SQL (e.g., migrator), always use parameterized binds `(?, ?)`.
- **Credential Storage**: Never hardcode API keys or SMTP passwords. Always pull from `.env` loaded via `Config`. Keep `.env` out of VCS (`.gitignore`).
- **SMTP Security**: Require TLS/SSL or STARTTLS for mail delivery transmission configurations.
- **Path Traversal Prevention**: Always validate paths using `DiskManager.resolve_path` to prevent reading/writing files outside the project root workspace directory.
