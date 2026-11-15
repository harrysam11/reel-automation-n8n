#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# Finance Reel Factory - RAW TERMUX Native Installer (Android)
# NO Docker, NO udocker, NO proot needed! 100% Native ARM64 execution.
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=================================================================="
echo "    Finance Reel Factory - Raw Termux Setup (Mobile Native)      "
echo "=================================================================="

# 1. Update Termux & Install pre-compiled binary packages
# Note: Installing python-pillow and python-numpy via pkg avoids pip compilation issues on Android!
echo "[1/4] Installing native Termux packages..."
pkg update -y
pkg install -y \
    python \
    python-pip \
    python-pillow \
    python-numpy \
    ffmpeg \
    libsndfile \
    libjpeg-turbo \
    libpng \
    git

# 2. Setup Storage Access (so rendered MP4 goes directly to Phone Gallery/Downloads)
if [ ! -d "$HOME/storage" ]; then
    echo "[2/4] Requesting Android storage permission..."
    termux-setup-storage || true
fi

# 3. Install remaining Python packages with --break-system-packages flag
# In Termux (Python 3.12+), --break-system-packages is required to allow pip package installation.
echo "[3/4] Installing Python dependencies..."
pip install --break-system-packages --no-cache-dir requests pydantic soundfile || {
    echo "Using python virtualenv fallback..."
    python3 -m venv "$HOME/.termux_reel_venv"
    source "$HOME/.termux_reel_venv/bin/activate"
    pip install requests pydantic soundfile
}

# 4. Create directories & generate brand placeholders
echo "[4/4] Setting up workspace & placeholders..."
mkdir -p BRAND TEMPLATES PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/{01_RESEARCH,02_SCRIPT,03_AUDIO,04_ASSETS/cat_reactions,04_ASSETS/charts,05_SLIDES,06_SUBTITLES,07_EDIT,08_EXPORT} OUTPUTS LOGS
python3 scripts/create_placeholders.py

echo ""
echo "=================================================================="
echo " Termux Native Setup Complete!"
echo " To generate a full reel on mobile, run:"
echo "   ./scripts/termux_run.sh"
echo "=================================================================="
