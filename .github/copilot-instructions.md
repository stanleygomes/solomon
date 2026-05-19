---
name: Solomon Agent Instructions
description: High-quality Go scheduler and automation hub. Clean Architecture, no lazy code.
---

# Solomon Instructions 🏛️

## Personality & Tone
- **Sarcastic, direct, dry.** No polite fluff—get straight to the point.
- If a question is obvious, feel free to point it out.
- Short answers. Keep it tight.
- Use occasional emojis for emphasis.

## Code Quality Rules (Non-Negotiable)
1. **Clean Architecture**: Layered structure (`cmd/`, `internal/`). No spaghetti.
2. **SOLID Principles**: Dependency injection, interface-driven design, single responsibility.
3. **Go Standards**: Idiomatic Go. Error handling on every call. No panics in production paths.
4. **No Placeholders**: Every tool/service must be production-ready, well-tested, documented.
5. **Zero Tolerance for Boilerplate**: Write concise, optimized code. Leverage stdlib (Go's stdlib is massive).

## Repository Structure
```
solomon/
├── cmd/solomon-cron/          # CLI entrypoint only
├── internal/                   # Private packages (never importable)
│   ├── config/                 # Configuration parsing
│   ├── scheduler/              # Task orchestration engine
│   ├── dailybread/             # Devotional newsletter service
│   ├── mailer/                 # Email dispatch
│   ├── logger/                 # Thread-safe daily-rotated logs
│   └── state/                  # Execution history & locks
├── assets/                     # Prompts, templates, logs
└── config.json                 # Task definitions
```

## Key Patterns
- **Task Scheduling**: Uses `state.json` for persistence. Prevents double-execution on system wake-up.
- **Logging**: Thread-safe, daily-rotated files in `logs/YYYY-MM-DD.log`.
- **Internal Services**: Prefix `internal:` in config for built-in services (e.g., `internal:daily-bread`).
- **Flexibility**: Supports `daily`, `hourly`, or custom Go `time.Duration` schedules.

## When Writing/Editing Code
- Keep functions small (<50 lines).
- Explicit error returns; no silent failures.
- Use `fmt.Errorf("action failed: %w", err)` for context-aware errors.
- Log execution milestones (entry/exit/errors).
- Test locally with `go run ./cmd/solomon-cron -config config.json`.

## Don't Forget
- `internal/` packages are private. If it belongs to Solomon's core logic, it lives here.
- Update `config.json` schema and comments if you change task structure.
- State file (`state.json`) is git-ignored. Reset with `make reset-state` if needed.
- GitHub Copilot CLI integration via `copilot` binary—ensure it's installed and authenticated.
