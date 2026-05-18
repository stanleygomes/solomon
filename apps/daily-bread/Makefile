# Daily Bread - Automation Makefile (Go Version)

# Default parameters (can be overridden on command call)
TEMPLATE ?= devocional

# Configure flags to pass to the Go executable
FLAGS = -template $(TEMPLATE)

.PHONY: run build list setup help

# Default command to compile and run today's newsletter
run:
	@go run main.go $(FLAGS)

# Compiles the optimized binary executable
build:
	@echo "Compiling Go binary..."
	@go build -o daily-bread main.go
	@echo "Done! Binary 'daily-bread' successfully generated."

# Installs/downloads Go module dependencies
setup:
	@echo "Fetching Go dependencies..."
	@go mod download
	@go mod tidy
	@echo "Done! Go dependencies successfully configured."

# Dynamically lists available prompts and templates
list:
	@echo "=================================================="
	@echo "  AVAILABLE PROMPTS (prompts/ directory)"
	@echo "=================================================="
	@ls -1 prompts/ | grep -v '^_' | sed 's/\.md//' | sed 's/^/ - /'
	@echo ""
	@echo "=================================================="
	@echo "  AVAILABLE TEMPLATES (templates/ directory)"
	@echo "=================================================="
	@ls -1 templates/ | sed 's/\.html//' | sed 's/^/ - /'
	@echo "=================================================="
	@echo "To run a specific template, use:"
	@echo "make run TEMPLATE=<name>"

# Displays help information about Makefile usage
help:
	@echo "=========================================================================="
	@echo "                 DAILY BREAD - LOCAL NEWSLETTER SYSTEM (GO)"
	@echo "=========================================================================="
	@echo "Useful commands:"
	@echo "  make setup                       - Downloads and tidies Go dependencies."
	@echo "  make build                       - Compiles the project into a local binary."
	@echo "  make list                        - Shows all current prompts and templates."
	@echo "  make run                         - Runs the default newsletter for today (devocional)."
	@echo "  make run TEMPLATE=personagem     - Runs study for a specific character."
	@echo "=========================================================================="
