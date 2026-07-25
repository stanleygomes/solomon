# Solomon Python Makefile (Modernizado com UV)

UV := uv

.PHONY: help install cli lint format clean seed cron logs

help:
	@echo "👑 Solomon - Automation Hub"
	@echo "┌─────────────────────┬────────────────────────────────────────┐"
	@echo "│ Command             │ Description                            │"
	@echo "├─────────────────────┼────────────────────────────────────────┤"
	@echo "│ make install        │ Setup project and install dependencies │"
	@echo "│ make cli            │ Run the interactive CLI chat command   │"
	@echo "│ make cron           │ Start the background cron daemon       │"
	@echo "│ make logs           │ Tail application and cron logs         │"
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
	$(UV) run src/cli/main.py chat

cron:
	@echo "⏰ Starting Solomon Cron Daemon..."
	@PYTHONPATH=src $(UV) run src/cron/main.py

logs:
	@echo "📋 Tailing Solomon logs (Ctrl+C to exit)..."
	@tail -f logs/*.log

seed:
	@echo "🌱 Seeding the database..."
	@PYTHONPATH=src $(UV) run src/core/database/seed.py

clean:
	rm -rf __pycache__ .pytest_cache .venv .uv
	find . -type d -name "__pycache__" -exec rm -rf {} +
