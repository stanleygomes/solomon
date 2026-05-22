# 👑 Solomon - AI & Automation Hub

**Solomon** is a lightweight, reliable task coordinator and automation hub written in **Python**. It's designed to run on personal machines (like laptops) that aren't online 24/7.

Unlike traditional cron engines that completely skip scheduled tasks if your computer is asleep during the designated hour, Solomon runs periodically (e.g., every 5 minutes) and uses a state file (`temp/state.json`) to track executions. This ensures your daily, hourly, or interval-based tasks run exactly once per scheduled period, no matter when your system boots, wakes, or sleeps.

## 📂 File Structure

```text
solomon/
├── main.py              # CLI entrypoint
├── core/                # Base & shared logic (infrastructure)
│   ├── ai.py            # AI Provider interface (GitHub Copilot CLI)
│   ├── config.py        # Dataclass-based config loader
│   ├── logger.py        # Daily rotated log writer
│   ├── mailer.py        # Generic SMTP client
│   └── state.py         # State manager (temp/state.json)
├── services/            # Business logic (internal services)
│   └── daily_bread.py   # Devotional newsletter generation service
├── scheduler/           # Orchestration engine
│   └── engine.py        # Decision and run logic (should_run)
├── assets/              # Prompts, HTML templates, assets
│   ├── prompts/         # MD prompts for AI services
│   └── templates/       # HTML layouts for emails
├── temp/                # Local data (git-ignored)
│   ├── logs/            # Daily log files
│   └── state.json       # Task execution state
├── config.json          # Task definitions and schedules
├── Makefile             # Automation shortcuts
└── requirements.txt     # Python dependencies
```

---

## ⚙️ Configuration (`config.json`)

Tasks are configured in the root `config.json` file.

### Properties:

- `id`: Unique identifier for state-tracking.
- `name`: Human-readable name for logging.
- `command`: Target executable, system command, or internal service prefixed with `internal:` (e.g., `internal:daily-bread`).
- `args`: Array of command-line arguments.
- `dir`: Working directory to execute the task in.
- `schedule`: `"daily"`, `"hourly"`, or custom intervals like `"12h"`, `"30m"`.

---

## 🚀 Execution & Automation

All shortcuts are centralized in the [Makefile](./Makefile):

### 1. Installation

Setup the Python virtual environment and install all dependencies:

```bash
make install
```

### 2. Manual Run

Run the coordinator check-and-execute routine:

```bash
make run
```

## 📅 System Integration (Setting Up your Local Cron)

To run the coordinator every 5 minutes under the hood, add Solomon to your user crontab:

```bash
crontab -e
```

And append the following entry (adjust paths to match your local setup):

```text
*/5 * * * * cd /home/stanley/projects/solomon && .venv/bin/python main.py > /dev/null 2>&1
```

Now, even if you close your laptop, tasks will be coordinated properly whenever the machine is active.

---

## 🍞 Integrated Service: Daily Bread

**Daily Bread** is a devotional generation service built directly into Solomon. It calls the **GitHub Copilot CLI** to generate deep reflections, compiles them into a clean HTML format, and emails them.

### ⚙️ Configuration & Environment

The application requires a `.env` file in the root directory. Copy the template provided in `.env.example` to start.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Made with 🔥 by Lumen HQ
