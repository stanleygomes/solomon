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

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_step() {
    echo -e "\n${BOLD}${BLUE}👉 Step $1: $2${NC}"
}

TARGET_DIR="${SOLOMON_DIR:-$HOME/.solomon}"
REPO_URL="https://github.com/stanleygomes/solomon.git"

echo -e "${BOLD}${GREEN}👑 Solomon - Initialization Script${NC}"
echo -e "----------------------------------"

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
    # Source local profile to populate PATH if needed, or we just rely on absolute path
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

# Step 5: Install Shell Alias
log_step "5" "Installing shell alias"
ALIAS_CMD="alias solomon=\"$TARGET_DIR/run_task.sh\""

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

# Try to source to make it available in current script context
if [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc" || true
fi
if [ -f "$HOME/.zshrc" ]; then
    source "$HOME/.zshrc" || true
fi

# Summary
echo -e "\n${BOLD}${GREEN}🎉 Solomon installation completed successfully!${NC}\n"
echo -e "  ⚙️  ${BOLD}Configure environment variables:${NC}"
echo -e "     edit: ${BOLD}$TARGET_DIR/.env${NC}\n"
echo -e "  🔄 ${BOLD}Activate the 'solomon' command in this terminal session:${NC}"
echo -e "     run:  ${BOLD}source ~/.bashrc${NC}  (or ${BOLD}source ~/.zshrc${NC})\n"
echo -e "  🚀 ${BOLD}Run tasks from anywhere:${NC}"
echo -e "     run:  ${BOLD}solomon run <task_name>${NC}\n"
