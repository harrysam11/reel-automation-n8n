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
echo " Running Automated Reel Platform: $PROJECT_ID"
echo "=================================================================="

# Check virtualenv if it was used
if [ -d "$HOME/.termux_reel_venv" ]; then
    source "$HOME/.termux_reel_venv/bin/activate"
fi

VOICE="${2:-hi-IN-MadhurNeural}"

# Run automated multi-video platform with real neural TTS & burned-in captions
python3 generate_new_reel.py --project "$PROJECT_ID" --voice "$VOICE"

# Export directly to Android Downloads folder
OUT_MP4="$PROJECT_DIR/08_EXPORT/reel_final.mp4"
OUT_ZIP="OUTPUTS/${PROJECT_ID}_DELIVERY_PACK.zip"

PHONE_DL="$HOME/storage/downloads"
if [ -d "$PHONE_DL" ]; then
    cp "$OUT_MP4" "$PHONE_DL/${PROJECT_ID}_final.mp4"
    cp "$OUT_ZIP" "$PHONE_DL/"
    echo ""
    echo "  -> Saved directly to Phone Gallery/Downloads:"
    echo "     $PHONE_DL/${PROJECT_ID}_final.mp4"
fi

echo ""
echo "=================================================================="
echo " Mobile Reel Ready!"
echo " Video: $OUT_MP4"
echo " (Ready to review and upload directly to Instagram from your phone!)"
echo "=================================================================="
