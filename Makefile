# Solomon Python Makefile (Modernizado com UV)

UV := uv

.PHONY: help install run api lint format clean

help:
	@echo "👑 Solomon - Automation Hub"
	@echo "┌─────────────────────┬────────────────────────────────────────┐"
	@echo "│ Command             │ Description                            │"
	@echo "├─────────────────────┼────────────────────────────────────────┤"
	@echo "│ make install        │ Setup project and install dependencies │"
	@echo "│ make run            │ Run the scheduler                      │"
	@echo "│ make api            │ Start the FastAPI server               │"
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

run:
	$(UV) run src/main.py $(task)

api:
	@echo "🚀 Starting Solomon API..."
	@echo "🌐 API URL:   http://127.0.0.1:8000"
	@echo "📖 API Docs:  http://127.0.0.1:8000/docs"
	@PYTHONPATH=src $(UV) run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

clean:
	rm -rf __pycache__ .pytest_cache .venv .uv
	find . -type d -name "__pycache__" -exec rm -rf {} +
