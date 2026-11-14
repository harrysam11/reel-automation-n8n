# wmill: python3
"""
Windmill script to generate editable PowerPoint slides for a reel.
"""
import os
import sys

# Ensure repository root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.generate_slides import create_deck

def main(project_id: str = "REEL_001_SIP_FD_REALITY_CHECK") -> dict:
    pptx_path = os.path.join(REPO_ROOT, "PROJECTS", project_id, "05_SLIDES", "reel_001_slides.pptx")
    create_deck(pptx_path)
    return {
        "success": True,
        "project_id": project_id,
        "pptx_file": pptx_path
    }
