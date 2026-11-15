#!/usr/bin/env python3
"""
Finance Reel Factory - Interactive Web Platform.
Features:
- Live Video Player (play & check before download)
- Ollama AI Script Assistant (draft, prompt, iterate & refine scripts)
- Model Manager (pull/download models from web UI)
- Template Selector (Hook, Comparison, Alert, Stat, Tier List, Outro)
- Real Neural Voice Synthesizer with burned-in subtitles
- One-click downloads (MP4 & delivery package)
"""
import os
import sys
import json
import asyncio
import subprocess
from typing import Optional, List
import requests
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from generate_new_reel import build_reel

app = FastAPI(title="Finance Reel Factory Studio")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "web", "static")), name="static")

OLLAMA_HOST = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

# ------------------------------------------------------------------------------
# Pydantic Request Models
# ------------------------------------------------------------------------------
class ScriptPromptRequest(BaseModel):
    prompt: str
    topic: Optional[str] = "Personal Finance"
    current_script: Optional[str] = ""
    model: Optional[str] = "llama3.2:1b"
    instruction: Optional[str] = "new"  # 'new' or 'refine'

class PullModelRequest(BaseModel):
    model: str

class RenderRequest(BaseModel):
    project_id: str
    title: str
    script_text: str
    voice: Optional[str] = "hi-IN-MadhurNeural"
    burn_subtitles: Optional[bool] = True

# ------------------------------------------------------------------------------
# Routes: Core Web Dashboard
# ------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    index_file = os.path.join(BASE_DIR, "web", "templates", "index.html")
    with open(index_file, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/system/status")
def get_system_status():
    ollama_ok = False
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=3)
        ollama_ok = (r.status_code == 200)
    except Exception:
        pass
        
    return {
        "status": "ready",
        "platform": "Finance Reel Factory Open-Source Studio",
        "ollama_connected": ollama_ok,
        "ollama_host": OLLAMA_HOST,
        "ffmpeg_available": bool(subprocess.run(["which", "ffmpeg"], capture_output=True).stdout),
        "workspace": BASE_DIR
    }

# ------------------------------------------------------------------------------
# Routes: Ollama AI Assistant
# ------------------------------------------------------------------------------
@app.get("/api/ollama/models")
def list_ollama_models():
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if r.status_code == 200:
            data = r.json()
            models = [m["name"] for m in data.get("models", [])]
            return {"models": models}
        return {"models": []}
    except Exception as e:
        return {"models": [], "error": str(e)}

@app.post("/api/ollama/pull")
def pull_ollama_model(req: PullModelRequest):
    try:
        # Start pull in Ollama
        r = requests.post(f"{OLLAMA_HOST}/api/pull", json={"name": req.model, "stream": False}, timeout=120)
        return {"success": True, "message": f"Model {req.model} pull status: {r.status_code}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ollama/generate_script")
def generate_ai_script(req: ScriptPromptRequest):
    system_prompt = (
        "You are an expert Indian finance content creator making high-retention 60-90 second Instagram Reels and YouTube Shorts. "
        "Tone: Savvy, humorous, sharp, disciplined. "
        "Style: Hinglish (natural spoken Hindi written in Devanagari or Latin script, with crisp English financial terms like SIP, FD, DICGC, CAGR, Index Fund). "
        "Rules: Keep sentences punchy and short. Include a shocking hook in the first 5 seconds, an explanation, a risk/reality check, and a clear follow CTA. "
        "Return ONLY the spoken narration lines, one paragraph per slide scene."
    )
    
    if req.instruction == "refine" and req.current_script:
        user_message = (
            f"Here is the current script:\n---\n{req.current_script}\n---\n"
            f"User Improvement Request: {req.prompt}\n"
            f"Please revise and improve the script based on this feedback."
        )
    else:
        user_message = f"Write a viral finance reel script about: {req.prompt}. Topic: {req.topic}"

    try:
        payload = {
            "model": req.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": False
        }
        r = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=60)
        if r.status_code == 200:
            content = r.json().get("message", {}).get("content", "")
            return {"success": True, "script": content}
        else:
            # Fallback if model not found
            return {
                "success": False,
                "error": f"Ollama error {r.status_code}. Is model '{req.model}' downloaded? You can pull it from the Model tab."
            }
    except Exception as e:
        return {"success": False, "error": f"Cannot connect to Ollama: {str(e)}"}

# ------------------------------------------------------------------------------
# Routes: Video Generation & Pipeline
# ------------------------------------------------------------------------------
@app.post("/api/render")
def trigger_render(req: RenderRequest):
    project_id = req.project_id.strip() or "REEL_NEW_PROJECT"
    proj_dir = os.path.join(BASE_DIR, "PROJECTS", project_id)
    os.makedirs(os.path.join(proj_dir, "02_SCRIPT"), exist_ok=True)
    
    # Save script
    script_path = os.path.join(proj_dir, "02_SCRIPT", "voiceover_clean.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(req.script_text)
        
    try:
        build_reel(
            project_id=project_id,
            title=req.title,
            voice=req.voice,
            burn_subtitles=req.burn_subtitles
        )
        video_url = f"/api/video/{project_id}"
        zip_url = f"/api/download/{project_id}"
        return {
            "success": True,
            "project_id": project_id,
            "video_url": video_url,
            "download_zip": zip_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Render error: {str(e)}")

# ------------------------------------------------------------------------------
# Routes: Video Streaming Player with Range Header
# ------------------------------------------------------------------------------
@app.get("/api/video/{project_id}")
def stream_video(project_id: str, request: Request):
    video_path = os.path.join(BASE_DIR, "PROJECTS", project_id, "08_EXPORT", "reel_final.mp4")
    if not os.path.exists(video_path):
        video_path = os.path.join(BASE_DIR, "PROJECTS", project_id, "08_EXPORT", "reel_001_final.mp4")
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
        
    file_size = os.path.getsize(video_path)
    range_header = request.headers.get("range")
    
    if range_header:
        # Byte-range request for smooth seeking in HTML5 video player
        bytes_str = range_header.replace("bytes=", "")
        start, end = bytes_str.split("-")
        start = int(start)
        end = int(end) if end else file_size - 1
        length = end - start + 1
        
        def iter_file():
            with open(video_path, "rb") as f:
                f.seek(start)
                bytes_left = length
                while bytes_left > 0:
                    chunk = f.read(min(bytes_left, 1024 * 64))
                    if not chunk:
                        break
                    bytes_left -= len(chunk)
                    yield chunk
                    
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(length),
            "Content-Type": "video/mp4",
        }
        return StreamingResponse(iter_file(), status_code=206, headers=headers)
        
    return FileResponse(video_path, media_type="video/mp4")

@app.get("/api/slides/{project_id}")
def get_slide_thumbnails(project_id: str):
    slides_dir = os.path.join(BASE_DIR, "PROJECTS", project_id, "05_SLIDES")
    if not os.path.exists(slides_dir):
        return {"slides": []}
    files = sorted([f for f in os.listdir(slides_dir) if f.startswith("slide-") and f.endswith(".png")])
    urls = [f"/api/slide_img/{project_id}/{f}" for f in files]
    return {"slides": urls}

@app.get("/api/slide_img/{project_id}/{slide_name}")
def get_slide_image(project_id: str, slide_name: str):
    img_path = os.path.join(BASE_DIR, "PROJECTS", project_id, "05_SLIDES", slide_name)
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail="Slide image not found")
    return FileResponse(img_path, media_type="image/png")

@app.get("/api/download/{project_id}")
def download_delivery_zip(project_id: str):
    zip_path = os.path.join(BASE_DIR, "OUTPUTS", f"{project_id}_DELIVERY_PACK.zip")
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="Delivery package not found")
    return FileResponse(zip_path, filename=f"{project_id}_DELIVERY_PACK.zip", media_type="application/zip")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    print(f"Starting Finance Reel Factory Studio on http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
