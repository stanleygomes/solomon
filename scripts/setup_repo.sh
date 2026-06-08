#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Load common logging and colors
setup_dir="${SOLOMON_DIR:-$HOME/.solomon}"
if [ -f "scripts/logger.sh" ]; then
  source "scripts/logger.sh"
elif [ -f "$setup_dir/scripts/logger.sh" ]; then
  source "$setup_dir/scripts/logger.sh"
else
  source <(curl -sSL https://raw.githubusercontent.com/stanleygomes/solomon/refs/heads/master/scripts/logger.sh)
fi

TARGET_DIR="$setup_dir"
REPO_URL="https://github.com/stanleygomes/solomon.git"

# Step 1: Clone or update the repository
log_step "1" "Cloning Solomon repository"
if [ -d "$TARGET_DIR" ]; then
  log_warning "Directory $TARGET_DIR already exists."
  log_info "Updating repository instead..."
  cd "$TARGET_DIR"
  git pull
  log_success "Repository updated."
else
  log_info "Cloning to $TARGET_DIR..."
  git clone "$REPO_URL" "$TARGET_DIR"
  cd "$TARGET_DIR"
  log_success "Repository cloned successfully."
fi

# Step 2: Ensure uv is installed
log_step "2" "Checking dependency manager (uv)"
UV_BIN=""
if command -v uv &> /dev/null; then
  UV_BIN="uv"
  log_success "uv is already installed on system PATH."
elif [ -f "$HOME/.local/bin/uv" ]; then
  UV_BIN="$HOME/.local/bin/uv"
  log_success "uv found at $UV_BIN."
else
  log_info "uv not found. Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  UV_BIN="$HOME/.local/bin/uv"
  log_success "uv installed successfully at $UV_BIN."
fi

# Step 3: Configure Environment Variables (.env)
log_step "3" "Configuring environment files"
if [ -f ".env" ]; then
  log_warning ".env file already exists. Skipping copy."
else
  log_info "No .env file found. Copying .env.example..."
  cp .env.example .env
  log_success ".env file created. Remember to edit it with your credentials!"
fi

# Step 4: Install Dependencies
log_step "4" "Installing project dependencies"
log_info "Running uv sync..."
"$UV_BIN" sync
log_success "Dependencies installed successfully."
