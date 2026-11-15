# Finance Reel Factory (Local-First Production Architecture)

A local-first, privacy-respecting video automation system for Indian finance reels. Built for Zorin OS / Linux with n8n orchestration, local TTS, editable PowerPoint slides (LibreOffice / python-pptx), and FFmpeg.

---

## 1. Directory Structure

```text
├── BRAND/
│   ├── brand_guide.txt              # Color palette (#F4EBDD), fonts, tone, rules
│   ├── main_cat.png                 # Sunglasses Cat mascot (Host)
│   └── logo.png                     # Reel Factory watermark logo
├── TEMPLATES/
│   ├── reel_brief.json              # Intake JSON schema & approval state
│   └── asset_manifest.csv           # Commercial rights & CC0 tracking
├── PROJECTS/
│   └── REEL_001_SIP_FD_REALITY_CHECK/
│       ├── 01_RESEARCH/sources.txt  # SEBI, AMFI, RBI, DICGC citations
│       ├── 02_SCRIPT/               # Tagged (directions) & clean voiceover scripts
│       ├── 03_AUDIO/                # voiceover.wav & voiceover_preview.mp3
│       ├── 04_ASSETS/               # Cat meme reactions & charts
│       ├── 05_SLIDES/               # Editable PPTX, PDF, and 1080x1920 PNG slides
│       ├── 06_SUBTITLES/            # Synchronized captions.srt
│       ├── 07_EDIT/                 # Concat playlists and composition files
│       ├── 08_EXPORT/               # Final rendered reel_001_final.mp4
│       └── scene_script.csv         # 12-scene timeline & visual cues
├── N8N/
│   ├── workflow_spec.md             # 6-workflow orchestration architecture
│   ├── node_map.csv                 # Node-by-node parameters and endpoints
│   └── workflows/
│       └── reel_factory_orchestrator.json # Ready-to-import n8n workflow
├── RESEARCH_SHORTLIST/
│   └── weekly_finance_shortlist.md  # 5 vetted Indian finance reel topics
├── scripts/
│   ├── generate_slides.py           # python-pptx 1080x1920 slide generator
│   ├── export_slides.sh             # Headless LibreOffice + pdftoppm exporter
│   ├── tts_generator.py             # Voice-over synthesizer
│   ├── render_video.py              # FFmpeg 1080x1920 30fps vertical MP4 assembler
│   ├── package_delivery.py          # Delivery packager (ZIP)
│   └── local_render_api.py          # Secure HTTP API bridge for n8n
└── OUTPUTS/
    └── REEL_001_SIP_FD_REALITY_CHECK_DELIVERY_PACK.zip
```

---

## 2. Quick Start: Install & Run

### A. One-Click Setup (Self-Hosted)
Run the automated installer to set up the Python venv, download the open Kokoro ONNX model weights, and verify system tools:
```bash
./scripts/install.sh
```

### B. Run the Full Reel Pipeline (One Command on PC)
Builds slides, exports PNGs, generates Kokoro voiceover, stitches the vertical MP4, and packages everything:
```bash
./scripts/run_all.sh
```

---

## 3. Mobile Setup: RAW TERMUX (Android Native)
**Zero Docker, Zero udocker, Zero proot needed!** Runs 100% natively on ARM64 Android.

### A. One-Time Setup in Termux
Inside your Termux terminal on Android:
```bash
# 1. Clone repository into Termux
git clone https://github.com/harrysam11/reel-automation-n8n.git
cd reel-automation-n8n

# 2. Run raw Termux native installer
chmod +x scripts/*.sh
./scripts/termux_install.sh
```

### B. Generate Reel Directly on Phone
```bash
./scripts/termux_run.sh
```
* **Instant Slide Rendering**: Uses `scripts/render_slides_native.py` via Pillow (100% native, zero LibreOffice required!).
* **ARM64 Accelerated Video**: Uses Termux's native NEON-accelerated FFmpeg.
* **Direct Export to Phone Downloads**: The rendered `1080x1920` MP4 reel is automatically placed in your phone's `Downloads` folder, ready to inspect, watch in your Gallery, and upload directly to Instagram!

---

## 4. Desktop Daemon & n8n Bridge (PC)
The 3 capital-map slides retain all 14 investment categories and indicative entry ranges:
- **Tier 1 (₹100 – ₹5,000):** Mutual Funds, ETFs, Direct Stocks, PPF/EPF/SSY, NPS, FDs/RDs.
- **Tier 2 (₹10,000 – ₹5 Lakh):** Government Securities (RBI Retail Direct), REITs/InvITs, SGB, Corporate Bonds/NCDs, P2P/Invoice Investing.
- **Tier 3 (₹20 Lakh – ₹1 Crore+):** Physical Real Estate, Portfolio Management Services (PMS - ₹50L SEBI minimum), Alternative Investment Funds (AIF - ₹1Cr SEBI minimum).

---

## 4. Asset Finder & Grabber Automation (WF-07)
A dedicated search and acquisition workflow for licensed/permissive media:
- **Search Query**: Queries Wikimedia Commons and CC repositories via API (`scripts/asset_finder.py search "<keyword>"`).
- **Download & Log**: Grabs high-resolution image to project assets and automatically records source URL, artist, and license type into `asset_manifest.csv` with `rights_verified: false` pending human sign-off.
- **Workflow File**: Available at [`N8N/workflows/asset_finder_workflow.json`](file:///home/sam/Documents/reel-automation-n8n/N8N/workflows/asset_finder_workflow.json).

---

## 5. n8n Security & Orchestration
- Does **not** require the dangerous `Execute Command` node inside the n8n Docker container.
- Connects over the local bridge to `scripts/local_render_api.py` running on `http://192.168.122.1:8085` with header authentication (`X-API-Key`).
- Workflow JSON is ready for import at [reel_factory_orchestrator.json](file:///home/sam/Documents/reel-automation-n8n/N8N/workflows/reel_factory_orchestrator.json).
