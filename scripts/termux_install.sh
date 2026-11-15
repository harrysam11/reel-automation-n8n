#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# Finance Reel Factory - RAW TERMUX Native Installer (Android)
# NO Docker, NO udocker, NO proot needed! 100% Native ARM64 execution.
# ==============================================================================
set -euo pipefail

echo "=================================================================="
echo "    Finance Reel Factory - Raw Termux Setup (Mobile Native)      "
echo "=================================================================="

# 1. Update Termux packages
echo "[1/4] Updating Termux packages..."
pkg update -y
pkg install -y python ffmpeg libsndfile libjpeg-turbo libpng clang git

# 2. Setup Storage Access (so rendered MP4 goes directly to Phone Gallery/Downloads)
if [ ! -d "$HOME/storage" ]; then
    echo "[2/4] Requesting Android storage permission..."
    termux-setup-storage || true
fi

# 3. Install Python packages natively
echo "[3/4] Installing Python packages (Pillow, soundfile, requests, etc.)..."
pip install --upgrade pip
pip install pillow requests pydantic soundfile numpy

# 4. Try installing kokoro-onnx (if ARM64 onnxruntime wheel is available)
echo "[4/4] Checking TTS engine..."
pip install kokoro-onnx || {
    echo "Notice: Standard kokoro-onnx requires aarch64 onnxruntime."
    echo "Fallback native TTS generator will be used if needed."
}

# 5. Create directories
mkdir -p BRAND TEMPLATES PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/{01_RESEARCH,02_SCRIPT,03_AUDIO,04_ASSETS/cat_reactions,04_ASSETS/charts,05_SLIDES,06_SUBTITLES,07_EDIT,08_EXPORT} OUTPUTS LOGS

echo ""
echo "=================================================================="
echo " Termux Native Setup Complete!"
echo " To generate a full reel on mobile, simply run:"
echo "   ./scripts/termux_run.sh"
echo "=================================================================="
