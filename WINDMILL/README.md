# Windmill Integration for Finance Reel Factory

An ultra-fast, Rust-based, code-first orchestrator alternative to n8n.

---

## 1. Why Windmill for this Setup?

1. **Native Python Execution**: Runs `scripts/generate_slides.py`, `scripts/tts_generator.py`, and `scripts/render_video.py` directly inside workers without needing the HTTP bridge daemon (`local_render_api.py`).
2. **Tiny RAM Footprint**: Windmill backend runs on **Rust** (~50–120 MB RAM vs 350 MB+ for Node.js/n8n).
3. **Mobile-First App Interface**: Automatically generates clean forms with buttons for your Android phone screen.

---

## 2. Quick Start on PC

Run the self-hosted Windmill stack using Docker Compose:

```bash
cd ~/Documents/reel-automation-n8n/WINDMILL
docker compose up -d
```

* **Windmill Web UI**: `http://localhost:8090` (on PC)
* **Mobile Access (from Android Phone)**: `http://192.168.0.105:8090` (same WiFi)
* **Initial Login**:
  * Email: `admin@windmill.dev`
  * Password: `changeme` (prompted to change on first login)

---

## 3. Directory Structure

```text
WINDMILL/
├── docker-compose.yml                  # Windmill Server + Worker + PostgreSQL
├── flows/
│   └── reel_factory_pipeline.flow/
│       └── flow.yaml                   # End-to-end DAG pipeline flow
├── scripts/
│   ├── generate_slides.py              # python-pptx slide generation step
│   ├── export_slides.py                # LibreOffice headless slide exporter
│   ├── generate_tts.py                 # Kokoro-82M TTS voiceover step
│   ├── render_video.py                 # FFmpeg vertical MP4 assembly step
│   └── package_delivery.py             # Android delivery packager
└── apps/
    └── reel_creator_app.json           # One-tap mobile control app
```

---

## 4. Triggering from Phone

1. Open `http://192.168.0.105:8090` in your phone's browser (Chrome/Brave).
2. Go to **Apps** -> **Finance Reel Factory - Mobile Creator App**.
3. Select your desired narrator voice (`hm_omega` for Hindi Male, `hf_alpha` for Hindi Female, `am_adam` for English).
4. Tap **🚀 Generate Reel Now**.
5. Watch the real-time execution steps and download the finished MP4 directly on your phone!
