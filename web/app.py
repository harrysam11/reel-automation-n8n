#!/usr/bin/env python3
"""
Finance Reel Factory - Complete Interactive Web Platform.
Features:
- Live 9:16 Video Player (Scrub & inspect before download)
- PPT Maker (1-Click Editable .pptx Presentation Deck)
- Local Ollama AI Script Assistant (Prompt, Iterate & "Thoda improve karo")
- Viral Hormozi-Style Captions (Electric Yellow, Thick Stroke, Emojis, 1-2 words)
- Expressive Neural Voiceover with SFX Layering (Whoosh & Boom)
- Viral Cat Meme Template Gallery & Internet Cat Search
- Multi-format delivery downloads (.mp4, .pptx, full .zip pack)
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

from engine.ppt_maker import build_pptx_deck, generate_slides_from_deck
from engine.tts_engine import synthesize_reel_audio
from engine.video_builder import render_reel_with_subtitles
from scripts.asset_finder import search_commons_assets, grab_asset

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

class InternetCatSearchRequest(BaseModel):
    query: Optional[str] = "funny cat meme"
    limit: Optional[int] = 6

class GrabCatRequest(BaseModel):
    asset_url: str
    cat_name: str

class RenderRequest(BaseModel):
    project_id: str
    title: str
    script_text: str
    voice: Optional[str] = "hi-IN-MadhurNeural"
    voice_style: Optional[str] = "viral_energetic"
    caption_style: Optional[str] = "electric_yellow"
    burn_subtitles: Optional[bool] = True
    cat_theme: Optional[str] = "viral_cats"

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
        r = requests.post(f"{OLLAMA_HOST}/api/pull", json={"name": req.model, "stream": False}, timeout=120)
        return {"success": True, "message": f"Model {req.model} pull status: {r.status_code}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ollama/generate_script")
def generate_ai_script(req: ScriptPromptRequest):
    system_prompt = (
        "You are an expert Indian finance content creator making high-retention 60-90 second Instagram Reels and YouTube Shorts. "
        "Tone: Savvy, humorous, sharp, energetic. "
        "Style: Hinglish (natural spoken Hindi in Devanagari or Latin script, with crisp English financial terms like SIP, FD, DICGC, CAGR, Index Fund). "
        "Rules: Keep sentences punchy, short, and dynamic. Include an attention-grabbing shock hook in the first 5 seconds, "
        "an explanation, a risk/reality check with math, and a clear follow CTA. "
        "Return ONLY the spoken narration lines."
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
            return {
                "success": False,
                "error": f"Ollama error {r.status_code}. Is model '{req.model}' downloaded? You can pull it from the Model tab."
            }
    except Exception as e:
        return {"success": False, "error": f"Cannot connect to Ollama: {str(e)}"}

# ------------------------------------------------------------------------------
# Routes: Cat Meme Templates & Internet Search
# ------------------------------------------------------------------------------
@app.get("/api/cats/templates")
def list_cat_templates():
    cats_dir = os.path.join(BASE_DIR, "assets", "cats")
    os.makedirs(cats_dir, exist_ok=True)
    files = sorted([f for f in os.listdir(cats_dir) if f.endswith((".png", ".jpg", ".jpeg"))])
    items = []
    for f in files:
        name = os.path.splitext(f)[0].replace("_", " ").title()
        items.append({
            "id": f,
            "name": name,
            "url": f"/api/cat_img/{f}"
        })
    return {"cats": items}

@app.get("/api/cat_img/{cat_name}")
def get_cat_image(cat_name: str):
    cat_path = os.path.join(BASE_DIR, "assets", "cats", cat_name)
    if not os.path.exists(cat_path):
        raise HTTPException(status_code=404, detail="Cat image not found")
    media = "image/png" if cat_name.endswith(".png") else "image/jpeg"
    return FileResponse(cat_path, media_type=media)

@app.post("/api/cats/fetch_internet")
def fetch_internet_cats(req: InternetCatSearchRequest):
    try:
        results = search_commons_assets(req.query, limit=req.limit or 6)
        return {"success": True, "results": results}
    except Exception as e:
        return {"success": False, "error": str(e), "results": []}

@app.post("/api/cats/grab")
def grab_cat_from_web(req: GrabCatRequest):
    try:
        clean_name = "".join([c if c.isalnum() else "_" for c in req.cat_name.lower()])[:30] + ".jpg"
        dest_rel = os.path.join("assets", "cats", clean_name)
        manifest = os.path.join("PROJECTS", "asset_manifest.csv")
        grab_asset(req.asset_url, dest_rel, manifest, category="viral_cat", notes="User web-grabbed cat meme")
        return {"success": True, "filename": clean_name, "url": f"/api/cat_img/{clean_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------------------------------------------------------
# Routes: Video & PPT Generation Pipeline
# ------------------------------------------------------------------------------
@app.post("/api/render")
def trigger_render(req: RenderRequest):
    project_id = req.project_id.strip() or "REEL_NEW_PROJECT"
    proj_dir = os.path.join(BASE_DIR, "PROJECTS", project_id)
    slides_dir = os.path.join(proj_dir, "05_SLIDES")
    audio_dir = os.path.join(proj_dir, "03_AUDIO")
    sub_dir = os.path.join(proj_dir, "06_SUBTITLES")
    export_dir = os.path.join(proj_dir, "08_EXPORT")
    
    for d in [slides_dir, audio_dir, sub_dir, export_dir, os.path.join(proj_dir, "02_SCRIPT")]:
        os.makedirs(d, exist_ok=True)
        
    # Save script
    script_path = os.path.join(proj_dir, "02_SCRIPT", "voiceover_clean.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(req.script_text)
        
    try:
        # 1. Build PowerPoint Deck (.pptx) & High-Res PNG Slides with Cat Memes
        pptx_path = os.path.join(slides_dir, f"{project_id}_presentation.pptx")
        build_pptx_deck(project_id, req.title, pptx_path, cat_theme=req.cat_theme or "viral_cats")
        slides = generate_slides_from_deck(project_id, req.title, slides_dir)
        
        # 2. Synthesize Expressive Audio with SFX
        audio_path = os.path.join(audio_dir, "voiceover.mp3")
        srt_path = os.path.join(sub_dir, "captions.srt")
        synthesize_reel_audio(
            text=req.script_text,
            output_audio=audio_path,
            output_srt=srt_path,
            voice_key=req.voice or "hi-IN-MadhurNeural",
            style_key=req.voice_style or "viral_energetic"
        )
        
        # 3. Assemble Vertical Video with Burned-in Hormozi-Style Captions
        out_mp4 = os.path.join(export_dir, "reel_final.mp4")
        render_reel_with_subtitles(
            slides_list=slides,
            audio_path=audio_path,
            srt_or_vtt_path=srt_path,
            output_mp4=out_mp4,
            burn_subtitles=req.burn_subtitles,
            caption_style=req.caption_style or "electric_yellow"
        )
        
        # 4. Package Delivery ZIP (including .pptx)
        zip_path = os.path.join(BASE_DIR, "OUTPUTS", f"{project_id}_DELIVERY_PACK.zip")
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        import zipfile
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(out_mp4, "video/reel_final.mp4")
            z.write(audio_path, "audio/voiceover.mp3")
            if os.path.exists(pptx_path):
                z.write(pptx_path, f"presentation/{os.path.basename(pptx_path)}")
            if os.path.exists(srt_path):
                z.write(srt_path, "subtitles/captions.srt")
            for s in slides:
                z.write(s, f"slides/{os.path.basename(s)}")

        return {
            "success": True,
            "project_id": project_id,
            "video_url": f"/api/video/{project_id}",
            "pptx_url": f"/api/pptx/{project_id}",
            "download_zip": f"/api/download/{project_id}"
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

@app.get("/api/pptx/{project_id}")
def download_pptx_deck(project_id: str):
    pptx_path = os.path.join(BASE_DIR, "PROJECTS", project_id, "05_SLIDES", f"{project_id}_presentation.pptx")
    if not os.path.exists(pptx_path):
        pptx_path = os.path.join(BASE_DIR, "PROJECTS", project_id, "05_SLIDES", "presentation.pptx")
    if not os.path.exists(pptx_path):
        pptx_path = os.path.join(BASE_DIR, "PROJECTS", project_id, "05_SLIDES", "reel_001_slides.pptx")
    if not os.path.exists(pptx_path):
        raise HTTPException(status_code=404, detail="PowerPoint deck not found. Generate reel first.")
    return FileResponse(
        pptx_path,
        filename=f"{project_id}_presentation.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

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
