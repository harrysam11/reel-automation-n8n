#!/usr/bin/env bash
# ==============================================================================
# Finance Reel Factory - Stop Web Studio Daemon
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PID_FILE="LOGS/web_studio.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "No Web Studio PID file found ($PID_FILE). Searching for active process..."
    pkill -f "web/app.py" 2>/dev/null || true
    echo "Done."
    exit 0
fi

PID=$(cat "$PID_FILE")
if kill -0 "$PID" >/dev/null 2>&1; then
    echo "Stopping Web Studio (PID $PID)..."
    kill "$PID" || kill -9 "$PID"
    rm -f "$PID_FILE"
    echo "Web Studio stopped successfully."
else
    echo "Web Studio was not running. Removed stale PID file."
    rm -f "$PID_FILE"
fi
