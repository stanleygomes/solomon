# Solomon Python Makefile

PYTHON := python3
PIP := pip3
VENV := .venv

.PHONY: help install run reset-state list run-daily-bread clean lint format

help:
	@echo "Solomon Cron - Python Version"
	@echo "Usage:"
	@echo "  make install           - Setup virtual environment and install dependencies"
	@echo "  make run               - Run the scheduler"
	@echo "  make run-daily-bread   - Force run the daily-bread task"
	@echo "  make lint              - Run linter (ruff) to check for issues"
	@echo "  make format            - Run formatter (ruff) to fix style and indentation"
	@echo "  make reset-state       - Clear the execution state (temp/state.json)"
	@echo "  make list              - List available prompts and templates"
	@echo "  make clean             - Remove cache and temporary files"

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/$(PIP) install -r requirements.txt
	$(VENV)/bin/$(PIP) install ruff

lint:
	$(VENV)/bin/ruff check .

format:
	$(VENV)/bin/ruff check . --fix
	$(VENV)/bin/ruff format .

run:
	$(VENV)/bin/$(PYTHON) main.py

run-daily-bread:
	$(VENV)/bin/$(PYTHON) main.py --run-task daily-bread

reset-state:
	rm -f temp/state.json
	@echo "State reset. All tasks will run on next execution."

clean:
	rm -rf __pycache__ .pytest_cache .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
