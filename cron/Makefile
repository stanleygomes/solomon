# Solomon Cron Scheduler - Automation Makefile

BINARY_NAME=solomon-cron

.PHONY: run build setup clean help test

# Default command to run the scheduler in-place
run:
	@go run .

# Compiles the optimized binary executable
build:
	@echo "Compiling Go binary..."
	@go build -o $(BINARY_NAME) .
	@echo "Done! Binary '$(BINARY_NAME)' successfully generated."

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
	@echo "                 SOLOMON CRON SCHEDULER (GO)"
	@echo "=========================================================================="
	@echo "Useful commands:"
	@echo "  make setup                       - Prepares module dependencies and creates log folder."
	@echo "  make build                       - Compiles the project into a local binary."
	@echo "  make run                         - Runs the scheduler immediately."
	@echo "  make reset-state                 - Resets state.json to force-run all tasks."
	@echo "  make clean                       - Removes compiled binary files."
	@echo "=========================================================================="
