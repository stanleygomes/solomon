# Solomon Python Makefile (Modernizado com UV)

UV := uv

.PHONY: help install cli api lint format clean seed cron

help:
	@echo "👑 Solomon - Automation Hub"
	@echo "┌─────────────────────┬────────────────────────────────────────┐"
	@echo "│ Command             │ Description                            │"
	@echo "├─────────────────────┼────────────────────────────────────────┤"
	@echo "│ make install        │ Setup project and install dependencies │"
	@echo "│ make cli            │ Start the Terminal User Interface (TUI)│"
	@echo "│ make api            │ Start the FastAPI server               │"
	@echo "│ make cron           │ Start the background cron daemon       │"
	@echo "│ make seed           │ Populate database with initial seeds   │"
	@echo "│ make lint           │ Run linter (ruff) to check for issues  │"
	@echo "│ make format         │ Run formatter (ruff) to fix style      │"
	@echo "│ make clean          │ Remove cache, venv and temporary files │"
	@echo "└─────────────────────┴────────────────────────────────────────┘"

install:
	$(UV) sync

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff check . --fix
	$(UV) run ruff format .

cli:
	$(UV) run src/cli/main.py

api:
	@echo "🚀 Starting Solomon API..."
	@echo "🌐 API URL:   http://127.0.0.1:7000"
	@echo "📖 API Docs:  http://127.0.0.1:7000/docs"
	@PYTHONPATH=src $(UV) run uvicorn api.main:app --host 0.0.0.0 --port 7000 --reload

cron:
	@echo "⏰ Starting Solomon Cron Daemon..."
	@PYTHONPATH=src $(UV) run src/cron/main.py

seed:
	@echo "🌱 Seeding the database..."
	@PYTHONPATH=src $(UV) run src/core/database/seed.py

clean:
	rm -rf __pycache__ .pytest_cache .venv .uv
	find . -type d -name "__pycache__" -exec rm -rf {} +
