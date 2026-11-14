# Termux (Android) + PC Hybrid Setup Guide (Option A)

Is setup me:
- **Android Phone (Termux)**: n8n orchestrator chalta hai. Aap phone ke browser (`http://localhost:5678`) se reels trigger karte hain aur approvals dete hain.
- **PC (Zorin OS)**: Heavy tasks karta hai (PowerPoint slides, Kokoro TTS, FFmpeg rendering).
- **Communication**: Phone ka n8n seedha PC ke Local Render API (`http://192.168.0.105:8085` ya Tailscale `http://100.123.109.16:8085`) ko call karta hai.

---

## 1. PC Par API Daemon Start Karna

Apne PC par repo ke andar ek command chalaiye:
```bash
cd ~/Documents/reel-automation-n8n
./scripts/start_api.sh
```
Aapka PC ab port `8085` par ready hai:
- **Home WiFi IP:** `http://192.168.0.105:8085`
- **Tailscale Mesh IP (Kahin se bhi):** `http://100.123.109.16:8085`

---

## 2. Phone Par Termux Setup (2 Options)

### Method 1: udocker ke zariye (Docker container inside Termux)

Termux open karke yeh commands run karein:
```bash
# 1. Termux packages update karein
pkg update -y && pkg install -y python proot curl

# 2. udocker install karein
pip install udocker
udocker install

# 3. n8n container pull aur run karein
udocker run -p 5678:5678 --name=n8n_mobile docker.n8n.io/n8nio/n8n:latest
```

---

### Method 2: Native Termux Node.js (Zyada Fast & Battery-Friendly)
Agar udocker me memory ya ptrace slow lage, toh native n8n Termux me direct chalta hai:
```bash
pkg install -y nodejs-lts python make clang
npm install -g n8n
n8n start
```

---

## 3. n8n Open Karein & Workflows Import Karein

1. Phone ke kisi bhi browser me open karein:
   `http://localhost:5678`
2. First-time setup complete karein (admin account create karein).
3. **Import Workflow**:
   - Menu me **Workflows** -> **Import from file** select karein.
   - Yeh do JSON files import karein (PC se phone par share karke ya direct paste karke):
     - `N8N/workflows/reel_factory_orchestrator.json`
     - `N8N/workflows/asset_finder_workflow.json`

---

## 4. Workflows Me PC Ka IP Set Karna

Workflow nodes me jahan URL hai, wahan:
- Same WiFi par hain toh: `http://192.168.0.105:8085`
- Ghar se bahar / Mobile data par hain (Tailscale): `http://100.123.109.16:8085`

Header me:
- `X-API-Key`: `reel-factory-secret-token-2026`

---

## 5. Reel Produce Karna & Review

1. n8n ke webhook par click karein ya "Execute Workflow" dabaiye.
2. PC turant background me slides banayega, Kokoro TTS audio generate karega, aur 1080x1920 video render karega.
3. Completed MP4 aur ZIP package direct aapke phone par review ke liye available ho jayega!
