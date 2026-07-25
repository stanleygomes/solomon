#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run shared repository setup (clones/updates repo, installs uv and deps, copies .env)
curl -sSL https://raw.githubusercontent.com/stanleygomes/solomon/refs/heads/master/scripts/setup_repo.sh | bash

TARGET_DIR="${SOLOMON_DIR:-$HOME/.solomon}"

# Load logging utilities from the cloned repository
source "$TARGET_DIR/scripts/logger.sh"

# Enter repository directory
cd "$TARGET_DIR"

# Resolve UV binary path
UV_BIN="uv"
if ! command -v uv &> /dev/null; then
  UV_BIN="$HOME/.local/bin/uv"
fi

# Step 5: Install shell function (idempotent)
log_step "5" "Installing shell launcher function"

# Using shell function instead of alias with subshell parentheses to avoid zsh parse error when arguments are passed
FUNC_CMD="solomon() { (cd \"$TARGET_DIR\" && PYTHONPATH=\"$TARGET_DIR/src\" \"$UV_BIN\" run \"$TARGET_DIR/src/cli/main.py\" \"\$@\"); }"

add_function_to_file() {
  local shell_rc="$1"
  local rc_dir="$(dirname "$shell_rc")"
  mkdir -p "$rc_dir"
  touch "$shell_rc"

  # Remove old alias if exists
  if grep -q "alias solomon=" "$shell_rc"; then
    log_info "Removing old alias from $shell_rc..."
    sed -i '/alias solomon=/d' "$shell_rc"
  fi

  # Add/update shell function
  if ! grep -q "solomon() {" "$shell_rc"; then
    echo -e "\n# Solomon CLI Launcher\n$FUNC_CMD" >> "$shell_rc"
    log_success "Function added to $shell_rc"
  else
    # Update function definition
    sed -i '/solomon() {/d' "$shell_rc"
    echo -e "$FUNC_CMD" >> "$shell_rc"
    log_info "Function updated in $shell_rc"
  fi
}

add_function_to_file "$HOME/.bashrc"
add_function_to_file "$HOME/.zshrc"

# Step 6: Seed the database (idempotent)
log_step "6" "Seeding the database"
log_info "Running database seed..."
PYTHONPATH=src "$UV_BIN" run src/core/database/seed.py
log_success "Database seeded."

# Step 7: Start Cron daemon (idempotent — skip if already running)
log_step "7" "Starting Cron daemon"
mkdir -p "$TARGET_DIR/logs"

CRON_SCRIPT="$TARGET_DIR/src/cron/main.py"
if pgrep -f "$CRON_SCRIPT" > /dev/null 2>&1; then
  log_info "Cron daemon is already running — skipping"
else
  nohup bash -c "PYTHONPATH=src $UV_BIN run $CRON_SCRIPT" \
      > "$TARGET_DIR/logs/cron.log" 2>&1 &
  CRON_PID=$!
  log_success "Cron daemon started (PID $CRON_PID)"
fi

# Summary
echo -e "\n${BOLD}${GREEN}🎉 Solomon is up and running!${NC}\n"
echo -e "  🚀 ${BOLD}Activate the 'solomon' command:${NC}"
if [ -n "$ZSH_VERSION" ] || [ "${SHELL##*/}" = "zsh" ]; then
  echo -e "     run: ${BOLD}source ~/.zshrc${NC}\n"
else
  echo -e "     run: ${BOLD}source ~/.bashrc${NC}\n"
fi
echo -e "  📋 ${BOLD}Logs:${NC}    $TARGET_DIR/logs/"
echo -e "  ⚙️  ${BOLD}Config:${NC}  edit $TARGET_DIR/.env\n"
