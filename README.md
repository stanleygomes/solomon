# 👑 solomon

A personal automation hub and task scheduler. Orchestrates daily workflows, integrates with AI models, compiles email templates, and exposes a CLI client and background Cron daemon.

Single-tenant, non-authenticated architecture designed to run directly on your server or local machine.

---

### 🚀 Server Setup & Installation

To deploy Solomon on your server, clone the repository, install dependencies, seed the database, register the global `solomon` CLI alias, and start the background Cron daemon:

```bash
curl -sSL https://raw.githubusercontent.com/stanleygomes/solomon/refs/heads/master/scripts/bootstrap.sh | bash
```

---

## 🏗️ Architecture

Solomon is split into three main modules:

| Module  | Description                                                         |
| ------- | ------------------------------------------------------------------- |
| `cli/`  | Typer-based CLI client — interactive workflow command runner (`solomon chat`) |
| `cron/` | Background daemon running scheduled jobs (APScheduler)              |
| `core/` | Shared domain logic — services, database, workflows                 |

---

## 🛠️ Development

All shortcuts are in the [Makefile](./Makefile).

### Installation

```bash
make install
```

### Running the CLI

Run interactive or direct chat commands:

```bash
make cli                         # Interactive mode: select action & input message

# Or run direct subcommands via uv:
uv run src/cli/main.py chat      # Interactive mode
uv run src/cli/main.py chat /daily-bread "good morning"  # Direct execution
uv run src/cli/main.py update    # Re-run bootstrap script to update installation
```

If installed via `bootstrap.sh`, use the global `solomon` command:

```bash
solomon chat
solomon chat /daily-bread
solomon update
```

### Database

```bash
make seed    # Run database migrations and seeders
```

### Background Cron Daemon, Status & Logs

```bash
make cron    # Start cron daemon in foreground
make status  # Check process status (RUNNING/STOPPED, PID, memory, uptime)
make logs    # Tail application and cron logs in real time
```

### Code Quality & Cleanup

```bash
make lint    # Check with ruff
make format  # Fix & format with ruff
make clean   # Remove cache, venv, temp files
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

---

## 💡 Workflows & Features

### @daily-bread

Generates and sends a daily Bible study via email.

1. Runs an AI prompt template (`daily-bread.md`)
2. Renders output into a styled HTML email (Jinja2 + themes)
3. Delivers via SMTP

> [!IMPORTANT]
> **Once-per-day lock**: Repeat executions on the same calendar day are skipped automatically via database log checks.

### @classes (Study Planner & Delivery)

Automated daily study routines for any topic.

- **Planning** — generates a structured syllabus for an `ACTIVE` course using an AI prompt, parses the response as JSON, and persists lessons in the database.
- **Execution** — retrieves the lesson for today, generates full content via AI, compiles a themed HTML email, sends it, and marks the lesson as completed.

---

## 🧰 Tech Stack

| Layer            | Technology                                                        |
| ---------------- | ----------------------------------------------------------------- |
| Runtime          | Python 3.14+ via **[uv](https://github.com/astral-sh/uv)**        |
| CLI              | **[Typer](https://github.com/fastapi/typer)** + **InquirerPy**    |
| Scheduler        | **[APScheduler](https://github.com/agronholm/apscheduler)**      |
| Persistence      | **SQLite** + **[Peewee ORM](https://github.com/coleifer/peewee)** |
| AI Orchestration | Custom multi-provider client (Copilot, Antigravity, etc.)         |
| Templates        | **[Jinja2](https://github.com/pallets/jinja2)**                   |
| Mail Delivery    | SMTP with TLS/STARTTLS                                            |
| Logging          | **[Loguru](https://github.com/Delgan/loguru)**                    |
| Code Quality     | **[Ruff](https://github.com/astral-sh/ruff)**                     |

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
