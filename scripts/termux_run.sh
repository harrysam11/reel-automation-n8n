#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# Finance Reel Factory - Raw Termux One-Click Runner (Mobile Native)
# Runs natively on Android without Docker/udocker/proot!
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PROJECT_ID="${1:-REEL_001_SIP_FD_REALITY_CHECK}"
PROJECT_DIR="PROJECTS/$PROJECT_ID"

echo "=================================================================="
echo " Running Native Reel Factory inside Termux: $PROJECT_ID"
echo "=================================================================="

echo ""
echo "[Step 1/4] Rendering 1080x1920 slides natively (Zero LibreOffice dependency)..."
python scripts/render_slides_native.py

echo ""
echo "[Step 2/4] Generating voiceover audio narration..."
python scripts/tts_generator.py

echo ""
echo "[Step 3/4] Assembling 1080x1920 MP4 vertical reel with Termux FFmpeg..."
python scripts/render_video.py

echo ""
echo "[Step 4/4] Bundling package and exporting to Android Storage..."
python scripts/package_delivery.py "$PROJECT_ID"

# Export directly to Android Downloads folder if storage permission exists
OUT_MP4="$PROJECT_DIR/08_EXPORT/reel_001_final.mp4"
OUT_ZIP="OUTPUTS/${PROJECT_ID}_DELIVERY_PACK.zip"

PHONE_DL="$HOME/storage/downloads"
if [ -d "$PHONE_DL" ]; then
    cp "$OUT_MP4" "$PHONE_DL/${PROJECT_ID}_final.mp4"
    cp "$OUT_ZIP" "$PHONE_DL/"
    echo "  -> Saved directly to Android Downloads: $PHONE_DL/${PROJECT_ID}_final.mp4"
fi

echo ""
echo "=================================================================="
echo " Mobile Reel Ready!"
echo " Video: $OUT_MP4"
echo " (Ready to review and upload directly to Instagram from your phone!)"
echo "=================================================================="
