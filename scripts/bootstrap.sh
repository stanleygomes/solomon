#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# ANSI Color Codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Helper functions for logging
log_info() {
  echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

log_step() {
  echo -e "\n${BOLD}${BLUE}👉 Step $1: $2${NC}"
}

TARGET_DIR="${SOLOMON_DIR:-$HOME/.solomon}"

# Run shared repository setup
curl -sSL https://raw.githubusercontent.com/stanleygomes/solomon/refs/heads/master/scripts/setup_repo.sh | bash

# Enter repository directory
cd "$TARGET_DIR"

# Resolve UV binary path
UV_BIN="uv"
if ! command -v uv &> /dev/null; then
  UV_BIN="$HOME/.local/bin/uv"
fi

# Step 5: Seed the database
log_step "5" "Seeding the database"
log_info "Running database seed..."
PYTHONPATH=src "$UV_BIN" run src/core/database/seed.py
log_success "Database seeded."

# Step 6: Start API server
log_step "6" "Starting API server"
mkdir -p "$TARGET_DIR/logs"
nohup bash -c "PYTHONPATH=src $UV_BIN run uvicorn api.main:app --host 0.0.0.0 --port 7000" \
    > "$TARGET_DIR/logs/api.log" 2>&1 &
API_PID=$!
log_success "API server started (PID $API_PID) → http://0.0.0.0:7000"

# Step 7: Start Cron daemon
log_step "7" "Starting Cron daemon"
nohup bash -c "PYTHONPATH=src $UV_BIN run src/cron/main.py" \
    > "$TARGET_DIR/logs/cron.log" 2>&1 &
CRON_PID=$!
log_success "Cron daemon started (PID $CRON_PID)"

# Summary
echo -e "\n${BOLD}${GREEN}🎉 Solomon server is up and running!${NC}\n"
echo -e "  🌐 ${BOLD}API:${NC}       http://0.0.0.0:7000"
echo -e "  📖 ${BOLD}API Docs:${NC}  http://0.0.0.0:7000/docs"
echo -e "  📋 ${BOLD}Logs:${NC}      $TARGET_DIR/logs/"
echo -e "  ⚙️  ${BOLD}Config:${NC}    edit $TARGET_DIR/.env\n"
