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

# Step 5: Install shell wrapper script in ~/.local/bin (cleanest solution for both bash & zsh)
log_step "5" "Installing solomon binary wrapper"

BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
WRAPPER_FILE="$BIN_DIR/solomon"

cat << EOF > "$WRAPPER_FILE"
#!/usr/bin/env bash
cd "$TARGET_DIR"
exec "$UV_BIN" run --directory "$TARGET_DIR" "$TARGET_DIR/src/cli/main.py" "\$@"
EOF

chmod +x "$WRAPPER_FILE"
log_success "Binary wrapper installed to $WRAPPER_FILE"

# Clean up legacy aliases or functions from rc files if present
clean_rc_file() {
  local shell_rc="$1"
  if [ -f "$shell_rc" ]; then
    sed -i '/alias solomon=/d' "$shell_rc"
    sed -i '/solomon()/d' "$shell_rc"
    sed -i '/# Solomon CLI/d' "$shell_rc"
  fi
}

clean_rc_file "$HOME/.bashrc"
clean_rc_file "$HOME/.zshrc"

# Ensure ~/.local/bin is in PATH in rc files if not already present
add_path_to_file() {
  local shell_rc="$1"
  local rc_dir="$(dirname "$shell_rc")"
  mkdir -p "$rc_dir"
  touch "$shell_rc"

  if ! grep -q 'PATH=.*\$HOME/\.local/bin' "$shell_rc" && ! grep -q 'PATH=.*\.local/bin' "$shell_rc"; then
    echo -e '\nexport PATH="$HOME/.local/bin:$PATH"' >> "$shell_rc"
    log_success "Added ~/.local/bin to PATH in $shell_rc"
  fi
}

add_path_to_file "$HOME/.bashrc"
add_path_to_file "$HOME/.zshrc"

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
