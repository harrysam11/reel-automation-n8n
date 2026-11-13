#!/usr/bin/env bash
# ==============================================================================
# Finance Reel Factory - One-Click Self-Hosted Installer
# Sets up Python virtualenv, dependencies, static FFmpeg, and Kokoro TTS weights.
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=== [1/5] Checking System Dependencies ==="
for cmd in python3 libreoffice pdftoppm curl tar; do
    if command -v "$cmd" >/dev/null 2>&1; then
        echo "  [OK] Found $cmd"
    else
        echo "  [WARNING] $cmd is not installed. Please install via: sudo apt install -y $cmd"
    fi
done

echo ""
echo "=== [2/5] Checking FFmpeg ==="
if command -v ffmpeg >/dev/null 2>&1; then
    echo "  [OK] FFmpeg found: $(ffmpeg -version | head -n 1)"
else
    echo "  -> FFmpeg not found in PATH. Installing static Linux build into ~/.local/bin..."
    mkdir -p "$HOME/.local/bin" /tmp/ffmpeg-install
    curl -fsSL https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ -C /tmp/ffmpeg-install --strip-components 1
    cp /tmp/ffmpeg-install/ffmpeg /tmp/ffmpeg-install/ffprobe "$HOME/.local/bin/"
    rm -rf /tmp/ffmpeg-install
    export PATH="$HOME/.local/bin:$PATH"
    echo "  [OK] Static FFmpeg installed successfully."
fi

echo ""
echo "=== [3/5] Setting up Python Virtual Environment ==="
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "  [OK] Created virtual environment at .venv/"
else
    echo "  [OK] Virtual environment exists at .venv/"
fi

source .venv/bin/activate
pip install --upgrade pip --quiet
echo "  -> Installing Python dependencies..."
pip install --quiet \
    python-pptx \
    pydantic \
    requests \
    Pillow \
    kokoro-onnx \
    soundfile \
    numpy

echo "  [OK] Python packages installed."

echo ""
echo "=== [4/5] Checking Kokoro TTS Model Weights ==="
mkdir -p models
if [ -f "models/kokoro-v1.0.onnx" ] && [ -f "models/voices-v1.0.bin" ]; then
    echo "  [OK] Kokoro ONNX model and voice weights present in models/"
else
    echo "  -> Downloading open-weight Kokoro model files (~338 MB)..."
    if [ ! -f "models/voices-v1.0.bin" ]; then
        curl -fL -o models/voices-v1.0.bin "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin"
    fi
    if [ ! -f "models/kokoro-v1.0.onnx" ]; then
        curl -fL -o models/kokoro-v1.0.onnx "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx"
    fi
    echo "  [OK] Kokoro weights downloaded."
fi

echo ""
echo "=== [5/5] Ensuring Workspace Directories & Placeholders ==="
mkdir -p BRAND TEMPLATES PROJECTS OUTPUTS LOGS N8N/workflows RESEARCH_SHORTLIST
python scripts/create_placeholders.py >/dev/null 2>&1 || true

echo ""
echo "=================================================================="
echo " Setup complete! You can now run:"
echo "   ./scripts/run_all.sh       # Runs the entire reel build pipeline"
echo "   ./scripts/start_api.sh     # Starts local API bridge for n8n"
echo "=================================================================="
