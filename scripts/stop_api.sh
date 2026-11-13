#!/usr/bin/env bash
# ==============================================================================
# Finance Reel Factory - Stop Local Render API Daemon
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PID_FILE="LOGS/render_api.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "Render API is not running (no PID file found)."
    exit 0
fi

PID=$(cat "$PID_FILE")
if kill -0 "$PID" >/dev/null 2>&1; then
    kill "$PID"
    echo "Stopped Render API process (PID: $PID)."
else
    echo "Process $PID was not running."
fi

rm -f "$PID_FILE"
