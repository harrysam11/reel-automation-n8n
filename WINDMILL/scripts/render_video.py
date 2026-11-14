# wmill: python3
"""
Windmill script to render final 1080x1920 30fps vertical MP4 using FFmpeg.
"""
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.render_video import render_reel

def main(project_id: str = "REEL_001_SIP_FD_REALITY_CHECK") -> dict:
    proj_dir = os.path.join(REPO_ROOT, "PROJECTS", project_id)
    output_mp4 = os.path.join(proj_dir, "08_EXPORT", "reel_001_final.mp4")
    
    render_reel(proj_dir, output_mp4)
    file_size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    
    return {
        "success": True,
        "project_id": project_id,
        "video_path": output_mp4,
        "file_size_mb": round(file_size_mb, 2),
        "resolution": "1080x1920",
        "fps": 30
    }
