# wmill: python3
"""
Windmill script to export PPTX slides to 1080x1920 PNGs using LibreOffice and pdftoppm.
"""
import os
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main(project_id: str = "REEL_001_SIP_FD_REALITY_CHECK") -> dict:
    pptx_path = os.path.join(REPO_ROOT, "PROJECTS", project_id, "05_SLIDES", "reel_001_slides.pptx")
    export_script = os.path.join(REPO_ROOT, "scripts", "export_slides.sh")
    
    res = subprocess.run([export_script, pptx_path], cwd=REPO_ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Slide export failed: {res.stderr}")
        
    slides_dir = os.path.join(REPO_ROOT, "PROJECTS", project_id, "05_SLIDES")
    pngs = [f for f in sorted(os.listdir(slides_dir)) if f.startswith("slide-") and f.endswith(".png")]
    return {
        "success": True,
        "project_id": project_id,
        "slide_count": len(pngs),
        "slides": pngs
    }
