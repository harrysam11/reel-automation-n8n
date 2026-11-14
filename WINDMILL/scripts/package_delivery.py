# wmill: python3
"""
Windmill script to package project deliverables into an Android/review ZIP bundle.
"""
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.package_delivery import package_delivery

def main(project_id: str = "REEL_001_SIP_FD_REALITY_CHECK") -> dict:
    package_delivery(project_id)
    zip_path = os.path.join(REPO_ROOT, "OUTPUTS", f"{project_id}_DELIVERY_PACK.zip")
    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    
    return {
        "success": True,
        "project_id": project_id,
        "zip_path": zip_path,
        "size_mb": round(size_mb, 2)
    }
