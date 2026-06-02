#!/bin/bash

# Solomon Task Cron Runner Wrapper
# Usage: ./run_task.sh <task_name>

set -e

# Resolve the project root directory (where this script is located)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if [ "$1" = "run" ]; then
  shift
fi

if [ -z "$1" ]; then
  echo "❌ Error: No task name provided." >&2
  echo "Usage: $0 [run] <task_name>" >&2
  exit 1
fi

TASK_NAME="$1"

# Locate uv binary
UV_BIN="/home/stanley/.local/bin/uv"
if [ ! -f "$UV_BIN" ]; then
  # Fallback to path lookup
  UV_BIN=$(which uv 2>/dev/null || echo "uv")
fi

echo "🚀 [Solomon Cron] Running task: $TASK_NAME"
exec "$UV_BIN" run src/main.py "$TASK_NAME"
