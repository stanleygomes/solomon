![solomon-banner](assets/logo/solomon-banner.png)

# 👑 solomon

A personal automation hub and task scheduler. Orchestrates daily workflows, integrates with AI models, compiles email templates, and exposes both an HTTP API and a Terminal User Interface (TUI) for management.

### 🚀 CLI Client Setup

To install the client and set up the global `solomon` command in your terminal:

```bash
curl -sSL https://raw.githubusercontent.com/stanleygomes/solomon/refs/heads/master/scripts/bootstrap_cli.sh | bash
```

### 🌐 Server Setup

To deploy the backend, seeds the database, and runs the API and Cron daemon in background:

```bash
curl -sSL https://raw.githubusercontent.com/stanleygomes/solomon/refs/heads/master/scripts/bootstrap.sh | bash
```

---

## 🏗️ Architecture

Solomon is split into four independent entrypoints:

| Module  | Description                                             |
| ------- | ------------------------------------------------------- |
| `api/`  | FastAPI HTTP server — chat, auth, and status routes     |
| `cli/`  | Typer-based CLI & Textual Terminal User Interface (TUI) |
| `cron/` | Background daemon running scheduled jobs                |
| `core/` | Shared domain logic — services, database, workflows     |

---

## 🛠️ Development

All shortcuts are in the [Makefile](./Makefile).

### Installation

```bash
make install
```

### Running

By default, the CLI launches the Textual TUI dashboard, but it also supports client-side subcommands (powered by `typer`):

```bash
make cli          # Launches the TUI Dashboard (default)

# Or run subcommands via uv:
uv run src/cli/main.py --help    # Show help and CLI usage
uv run src/cli/main.py status    # Check status of the remote API
uv run src/cli/main.py update    # Update the Solomon CLI to the latest version
uv run src/cli/main.py config    # Configure local settings (API host URL, etc.)
```

If you installed the CLI via the quick start script, you can use the global `solomon` command:

```bash
solomon --help
solomon status
solomon update
solomon config
```

### Database

```bash
make seed    # Populate with initial seeds
```

### Code Quality

```bash
make lint    # Check with ruff
make format  # Fix & format with ruff
```

### Cleanup

```bash
make clean   # Remove cache, venv, temp files
```

### ⚙️ Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

---

## 💡 Features

### @daily-bread

Generates and sends a daily Bible study via email.

1. Runs an AI prompt template (`daily-bread.md`)
2. Renders output into a styled HTML email (Jinja2 + themes)
3. Delivers via SMTP

> [!IMPORTANT]
> **Once-per-day lock**: Repeat executions on the same calendar day are skipped automatically via database log checks.

Triggered by the cron daemon or manually:

```bash
make cron
```

### @classes (Study Planner & Delivery)

Automated daily study routines for any topic.

**Planning** — generates a structured syllabus for an `ACTIVE` course using an AI prompt, parses the response as JSON, and persists lessons in the database.

**Execution** — retrieves the lesson for today, generates full content via AI, compiles a themed HTML email, sends it, and marks the lesson as completed.

---

## 🔌 API

The FastAPI server exposes an OpenAI-compatible chat interface and authentication endpoints.

- **Docs**: `http://127.0.0.1:7000/docs`
- **Auth**: Magic Code + JWT (RS256) — passwordless, cookie-based sessions
- **Rate Limiting**: Configurable via `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW_SECONDS`

---

## 🧰 Tech Stack

| Layer            | Technology                                                        |
| ---------------- | ----------------------------------------------------------------- |
| Runtime          | Python 3.14+ via **[uv](https://github.com/astral-sh/uv)**        |
| API              | **FastAPI** + **Uvicorn**                                         |
| TUI              | **[Textual](https://github.com/Textualize/textual)**              |
| Persistence      | **SQLite** + **[Peewee ORM](https://github.com/coleifer/peewee)** |
| AI Orchestration | Custom multi-provider client (Copilot, Antigravity, etc.)         |
| Templates        | **[Jinja2](https://github.com/pallets/jinja2)**                   |
| Mail Delivery    | SMTP with TLS/STARTTLS                                            |
| Logging          | **[Loguru](https://github.com/Delgan/loguru)**                    |
| Auth             | **PyJWT** (RS256) + Magic Code verification                       |
| Code Quality     | **[Ruff](https://github.com/astral-sh/ruff)**                     |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
