#!/usr/bin/env bash
# ==============================================================================
# Finance Reel Factory - Start Local Render API Daemon
# Runs scripts/local_render_api.py in the background for n8n integration.
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PID_FILE="LOGS/render_api.pid"
LOG_FILE="LOGS/render_api.log"
mkdir -p LOGS

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" >/dev/null 2>&1; then
        echo "Render API is already running with PID $PID."
        echo "Logs: $LOG_FILE"
        exit 0
    else
        rm -f "$PID_FILE"
    fi
fi

source .venv/bin/activate
nohup python scripts/local_render_api.py >> "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo "$NEW_PID" > "$PID_FILE"

sleep 1
if kill -0 "$NEW_PID" >/dev/null 2>&1; then
    echo "Render API daemon started successfully with PID $NEW_PID."
    echo "Listening on: http://0.0.0.0:8085"
    echo "Logs: $LOG_FILE"
else
    echo "Failed to start Render API. Check $LOG_FILE for details."
    exit 1
fi
