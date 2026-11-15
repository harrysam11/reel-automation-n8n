#!/usr/bin/env bash
# ==============================================================================
# Finance Reel Factory - Interactive Web Studio Launcher
# Starts Ollama (if not running) + FastAPI Web Studio on port 5000
# Accessible on PC (localhost:5000) and Phone (LAN/Tailscale IP:5000)
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PID_FILE="LOGS/web_studio.pid"
LOG_FILE="LOGS/web_studio.log"
mkdir -p LOGS

# 1. Check & Start Ollama if needed
if ! curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    echo "Starting local Ollama server in background..."
    nohup /usr/local/bin/ollama serve >> LOGS/ollama.log 2>&1 &
    sleep 2
fi

# 2. Check if Studio is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" >/dev/null 2>&1; then
        echo "Web Studio is already running with PID $PID."
        echo "Access URLs:"
        echo "  • PC Local:   http://localhost:5000"
        echo "  • Phone/LAN:  http://$(hostname -I | awk '{print $1}'):5000"
        exit 0
    else
        rm -f "$PID_FILE"
    fi
fi

# 3. Launch Web Studio FastAPI app
echo "Starting Finance Reel Factory Web Studio..."
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

nohup "$PYTHON_BIN" "$ROOT_DIR/web/app.py" </dev/null >> "$LOG_FILE" 2>&1 &
NEW_PID=$!
disown "$NEW_PID" 2>/dev/null || true
echo "$NEW_PID" > "$PID_FILE"

sleep 2
if kill -0 "$NEW_PID" >/dev/null 2>&1; then
    echo "=========================================================="
    echo "  🎉 Finance Reel Factory Studio is RUNNING (PID $NEW_PID)"
    echo "=========================================================="
    echo "  • PC Browser:       http://localhost:5000"
    echo "  • Phone / WiFi LAN: http://$(hostname -I | awk '{print $1}'):5000"
    echo "  • Tailscale IP:     http://100.123.109.16:5000"
    echo "  • Studio Logs:      $ROOT_DIR/$LOG_FILE"
    echo "=========================================================="
    echo "To stop the studio, run: ./scripts/stop_studio.sh"
else
    echo "Failed to start Web Studio. Check $LOG_FILE for details."
    exit 1
fi
