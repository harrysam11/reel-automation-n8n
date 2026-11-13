# n8n Reel Factory — Workflow Specification

## Overview
The Reel Factory automation is designed as a modular pipeline controlled entirely by n8n.
To satisfy strict local-first security:
- **No Execute Command node** is required inside Docker.
- Communication with host renderers (PowerPoint generator, LibreOffice headless, TTS, and FFmpeg) occurs via authenticated HTTP requests to the private Host Render API (`http://192.168.122.1:8085`).
- The pipeline enforces **human-in-the-loop approval gates** for financial accuracy, asset licensing, audio review, and final packaging.

---

## 1. Six Production Workflows

### WF-01: Reel Intake & Validation
- **Trigger:** Webhook or Manual Form trigger (Project ID, Title, Target Duration, Topic).
- **Actions:**
  1. Validates project schema against `TEMPLATES/reel_brief.json`.
  2. Creates project directories (`01_RESEARCH` to `08_EXPORT`).
  3. Initializes `asset_manifest.csv` and `scene_script.csv`.
- **Gate:** Automated folder and manifest verification.

### WF-02: Research & Script Drafting
- **Trigger:** Intake completion.
- **Actions:**
  1. Compiles research references into `01_RESEARCH/sources.txt`.
  2. Optional local LLM draft via Ollama (`http://192.168.122.1:11434`).
  3. Formats `voiceover_tagged.txt` and `voiceover_clean.txt`.
- **Gate 1 (Human Approval):** Verification of SEBI/RBI/AMFI regulatory claims before audio or slides proceed.

### WF-03: Asset & Slide Builder
- **Trigger:** Script Approval webhook.
- **Actions:**
  1. Rights verification check against `TEMPLATES/asset_manifest.csv`.
  2. Calls Host Render API: `POST /api/generate-slides` (executes `scripts/generate_slides.py`).
  3. Calls Host Render API: `POST /api/export-slides` (LibreOffice + pdftoppm to PNG).
- **Gate 2 (Human Approval):** Visual check of 1080x1920 slide PNG deck.

### WF-04: Voice-over Generator
- **Trigger:** Script & Slide approval.
- **Actions:**
  1. Sends clean script segments to Host Render API: `POST /api/generate-audio`.
  2. Generates `voiceover.wav` and compressed `voiceover_preview.mp3`.
  3. Prepares synchronized `captions.srt`.
- **Gate 3 (Human Approval):** Audio audition for Hindi pronunciation and pacing.

### WF-05: Video Renderer
- **Trigger:** Audio approval.
- **Actions:**
  1. Calls Host Render API: `POST /api/render-video`.
  2. FFmpeg stitches slides + audio + subtitles into 1080x1920 30fps H.264 MP4.
  3. Runs technical validation (aspect ratio, audio sync, frame rate).
- **Gate 4 (Human Approval):** Final MP4 review.

### WF-06: Final Delivery & Packaging
- **Trigger:** Video approval.
- **Actions:**
  1. Calls Host Render API: `POST /api/package-delivery`.
  2. Bundles MP4, PPTX, PDF, WAV, MP3, SRT, and manifests into `OUTPUTS/{PROJECT_ID}_DELIVERY_PACK.zip`.
  3. Prepares files for Android USB / local transfer.

---

## 2. Asset Finder & Grabber Sub-Workflow (WF-07)
- **Trigger:** Webhook `POST /asset-search` with search query (e.g. "shocked cat", "gold bar chart").
- **Actions:**
  1. Calls Host Render API: `POST /api/find-assets` to search Wikimedia Commons / Openverse APIs.
  2. Extracts high-resolution image URLs, dimensions, license types (CC0, CC-BY, Public Domain), and attribution.
  3. Formats candidates for human preview.
  4. Webhook `POST /asset-grab` downloads the selected candidate to `04_ASSETS/cat_reactions/` or `charts/`.
  5. Automatically appends the asset ID, local path, source URL, and license terms to `TEMPLATES/asset_manifest.csv` with `rights_verified=false` pending approval.
