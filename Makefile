# Solomon Python Makefile

PYTHON := python3
PIP := pip3
VENV := .venv

.PHONY: help install run reset-state list run-daily-bread clean

help:
	@echo "Solomon Cron - Python Version"
	@echo "Usage:"
	@echo "  make install           - Setup virtual environment and install dependencies"
	@echo "  make run               - Run the scheduler"
	@echo "  make run-daily-bread   - Force run the daily-bread task"
	@echo "  make reset-state       - Clear the execution state (state.json)"
	@echo "  make list              - List available prompts and templates"
	@echo "  make clean             - Remove cache and temporary files"

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/$(PIP) install -r requirements.txt

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
