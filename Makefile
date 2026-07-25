# Solomon Python Makefile (Modernizado com UV)

UV := uv

.PHONY: help install cli lint format clean seed cron logs status

help:
	@echo "👑 Solomon - Automation Hub"
	@echo "┌─────────────────────┬────────────────────────────────────────┐"
	@echo "│ Command             │ Description                            │"
	@echo "├─────────────────────┼────────────────────────────────────────┤"
	@echo "│ make install        │ Setup project and install dependencies │"
	@echo "│ make cli            │ Run the interactive CLI chat command   │"
	@echo "│ make status         │ Check background daemon process status │"
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

status:
	@echo "🔍 Checking Solomon Cron Daemon Status..."
	@PID=$$(pgrep -f "src/cron/main.py" | head -n 1); \
	if [ -n "$$PID" ]; then \
		echo "✅ Status:  RUNNING (PID $$PID)"; \
		echo "📊 Memory:  $$(ps -o rss= -p $$PID | awk '{print int($$1/1024)" MB"}')"; \
		echo "⏱️ Uptime:  $$(ps -o etime= -p $$PID | xargs)"; \
		echo "📋 Log file: $$(pwd)/logs/cron.log"; \
	else \
		echo "❌ Status:  STOPPED (Cron daemon is not running)"; \
	fi

logs:
	@echo "📋 Tailing Solomon logs (Ctrl+C to exit)..."
	@tail -f logs/*.log

seed:
	@echo "🌱 Seeding the database..."
	@PYTHONPATH=src $(UV) run src/core/database/seed.py

clean:
	rm -rf __pycache__ .pytest_cache .venv .uv
	find . -type d -name "__pycache__" -exec rm -rf {} +
