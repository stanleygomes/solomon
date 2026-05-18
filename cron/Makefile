# Solomon Cron Scheduler - Automation Makefile

BINARY_NAME=solomon-cron
TEMPLATE ?= devocional

.PHONY: run build setup clean help reset-state run-daily-bread list

# Default command to run the scheduler in-place
run:
	@go run ./cmd/solomon-cron

# Compiles the optimized binary executable
build:
	@echo "Compiling Go binary..."
	@go build -o $(BINARY_NAME) ./cmd/solomon-cron
	@echo "Done! Binary '$(BINARY_NAME)' successfully generated."

# Runs the daily-bread devotional newsletter force-executing the internal service
run-daily-bread:
	@go run ./cmd/solomon-cron -run-task daily-bread -template $(TEMPLATE)

# Dynamically lists available prompts and templates for daily-bread
list:
	@echo "=================================================="
	@echo "  AVAILABLE PROMPTS (assets/prompts/ directory)"
	@echo "=================================================="
	@ls -1 assets/prompts/ | grep -v '^_' | sed 's/\.md//' | sed 's/^/ - /'
	@echo ""
	@echo "=================================================="
	@echo "  AVAILABLE TEMPLATES (assets/templates/ directory)"
	@echo "=================================================="
	@ls -1 assets/templates/ | sed 's/\.html//' | sed 's/^/ - /'
	@echo "=================================================="
	@echo "To run a specific template, use:"
	@echo "make run-daily-bread TEMPLATE=<name>"
	@echo "=================================================="

# Installs/downloads Go module dependencies and sets up directories
setup:
	@echo "Configuring Go dependencies..."
	@go mod tidy
	@mkdir -p logs
	@echo "Done! Setup completed."

# Removes the compiled binary and local state for a fresh test run
clean:
	@echo "Cleaning compiled artifacts..."
	@rm -f $(BINARY_NAME)
	@echo "Done!"

# Helper task to reset the scheduler execution state (for debugging and manual force-runs)
reset-state:
	@echo "Resetting execution state file (state.json)..."
	@rm -f state.json
	@echo "State successfully reset."

# Displays help information about Makefile usage
help:
	@echo "=========================================================================="
	@echo "                 SOLOMON CRON SCHEDULER & SERVICES (GO)"
	@echo "=========================================================================="
	@echo "Useful commands:"
	@echo "  make setup                       - Prepares module dependencies and creates log folder."
	@echo "  make build                       - Compiles the project into a local binary."
	@echo "  make run                         - Runs the scheduler immediately."
	@echo "  make reset-state                 - Resets state.json to force-run all tasks."
	@echo "  make clean                       - Removes compiled binary files."
	@echo "=========================================================================="
	@echo "Services (Daily Bread Devotional Newsletter):"
	@echo "  make list                        - Shows all templates/prompts in assets/."
	@echo "  make run-daily-bread             - Dispatches the daily devotional (devocional)."
	@echo "  make run-daily-bread TEMPLATE=x  - Dispatches study using template 'x'."
	@echo "=========================================================================="
