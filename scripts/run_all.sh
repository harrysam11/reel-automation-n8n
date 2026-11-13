#!/usr/bin/env bash
# ==============================================================================
# Finance Reel Factory - One-Command Full Pipeline Runner
# Builds slides, exports PNGs, generates Kokoro audio, renders MP4, and packages delivery.
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run ./scripts/install.sh first."
    exit 1
fi

source .venv/bin/activate
PROJECT_ID="${1:-REEL_001_SIP_FD_REALITY_CHECK}"
PROJECT_DIR="PROJECTS/$PROJECT_ID"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory '$PROJECT_DIR' does not exist."
    exit 1
fi

echo "=================================================================="
echo " Starting Full Reel Pipeline for: $PROJECT_ID"
echo "=================================================================="

echo ""
echo "[Step 1/5] Generating editable PowerPoint slides..."
python scripts/generate_slides.py

echo ""
echo "[Step 2/5] Exporting slides to 1080x1920 PNGs (LibreOffice + pdftoppm)..."
./scripts/export_slides.sh "$PROJECT_DIR/05_SLIDES/reel_001_slides.pptx"

echo ""
echo "[Step 3/5] Generating offline voiceover narration with Kokoro-82M TTS..."
python scripts/tts_generator.py

echo ""
echo "[Step 4/5] Assembling 1080x1920 vertical MP4 video with FFmpeg..."
python scripts/render_video.py

echo ""
echo "[Step 5/5] Packaging delivery ZIP for Android / local review..."
python scripts/package_delivery.py "$PROJECT_ID"

echo ""
echo "=================================================================="
echo " Pipeline Complete!"
echo " Output Video: $PROJECT_DIR/08_EXPORT/reel_001_final.mp4"
echo " Delivery Zip: OUTPUTS/${PROJECT_ID}_DELIVERY_PACK.zip"
echo "=================================================================="
