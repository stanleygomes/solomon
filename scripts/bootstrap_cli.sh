#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# ANSI Color Codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
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

# Resolve UV binary path
UV_BIN="uv"
if ! command -v uv &> /dev/null; then
  UV_BIN="$HOME/.local/bin/uv"
fi

# Step 5: Install Shell Alias
log_step "5" "Installing shell alias"
ALIAS_CMD="alias solomon=\"PYTHONPATH=$TARGET_DIR/src $UV_BIN run $TARGET_DIR/src/cli/main.py\""

add_alias_to_file() {
  local shell_rc="$1"
  if [ -f "$shell_rc" ]; then
    if ! grep -q "alias solomon=" "$shell_rc"; then
      echo -e "\n# Solomon Task Runner Alias\n$ALIAS_CMD" >> "$shell_rc"
      log_success "Alias added to $shell_rc"
    else
      log_info "Alias already exists in $shell_rc"
    fi
  fi
}

add_alias_to_file "$HOME/.bashrc"
add_alias_to_file "$HOME/.zshrc"

# Summary
echo -e "\n${BOLD}${GREEN}🎉 Solomon CLI installation completed successfully!${NC}\n"
echo -e "  🔄 ${BOLD}Activate the 'solomon' command in this terminal session:${NC}"
echo -e "     run:  ${BOLD}source ~/.bashrc${NC}  (or ${BOLD}source ~/.zshrc${NC})\n"
echo -e "  🚀 ${BOLD}Run tasks from anywhere:${NC}"
echo -e "     run:  ${BOLD}solomon --help${NC}"
echo -e "     run:  ${BOLD}solomon status${NC}"
echo -e "     run:  ${BOLD}solomon tui${NC}\n"
