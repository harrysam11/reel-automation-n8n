#!/usr/bin/env bash
# Convert PPTX to PDF via LibreOffice, then PDF to PNG via pdftoppm
set -euo pipefail

PPTX_FILE="${1:-PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/05_SLIDES/reel_001_slides.pptx}"
OUT_DIR="$(dirname "$PPTX_FILE")"

if [ ! -f "$PPTX_FILE" ]; then
    echo "Error: Slide presentation not found at $PPTX_FILE"
    exit 1
fi

echo "[1/2] Converting PPTX to PDF using LibreOffice headless..."
libreoffice --headless --convert-to pdf "$PPTX_FILE" --outdir "$OUT_DIR"

PDF_FILE="${PPTX_FILE%.pptx}.pdf"

echo "[2/2] Exporting PDF pages to 1080x1920 PNG slides..."
# Convert at 120 DPI (9 inches x 120 dpi = 1080 px width, 16 inches x 120 dpi = 1920 px height!)
pdftoppm -png -r 120 "$PDF_FILE" "$OUT_DIR/slide"

echo "Slides successfully exported to $OUT_DIR/slide-*.png"
ls -la "$OUT_DIR"/slide-*.png
