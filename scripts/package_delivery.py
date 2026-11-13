#!/usr/bin/env python3
"""
Package delivery files for Android review and manual publishing.
Creates an organized ZIP bundle under OUTPUTS/.
"""
import os
import zipfile
import shutil

def package_delivery(project_id="REEL_001_SIP_FD_REALITY_CHECK"):
    base_dir = os.path.join("PROJECTS", project_id)
    output_zip = os.path.join("OUTPUTS", f"{project_id}_DELIVERY_PACK.zip")
    os.makedirs("OUTPUTS", exist_ok=True)
    
    files_to_pack = [
        # Exported MP4
        ("08_EXPORT/reel_001_final.mp4", "video/reel_001_final.mp4"),
        # Editable PPTX & PDF
        ("05_SLIDES/reel_001_slides.pptx", "slides/reel_001_slides.pptx"),
        ("05_SLIDES/reel_001_slides.pdf", "slides/reel_001_slides.pdf"),
        # Audio
        ("03_AUDIO/voiceover.wav", "audio/voiceover.wav"),
        ("03_AUDIO/voiceover_preview.mp3", "audio/voiceover_preview.mp3"),
        # Subtitles
        ("06_SUBTITLES/captions.srt", "subtitles/captions.srt"),
        # Scripts
        ("02_SCRIPT/voiceover_tagged.txt", "scripts/voiceover_tagged.txt"),
        ("02_SCRIPT/voiceover_clean.txt", "scripts/voiceover_clean.txt"),
        ("scene_script.csv", "scripts/scene_script.csv"),
        # Research
        ("01_RESEARCH/sources.txt", "research/sources.txt"),
        # Manifest
        ("../../TEMPLATES/asset_manifest.csv", "metadata/asset_manifest.csv"),
        ("../../TEMPLATES/reel_brief.json", "metadata/reel_brief.json")
    ]
    
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for rel_src, arcname in files_to_pack:
            full_src = os.path.normpath(os.path.join(base_dir, rel_src))
            if os.path.exists(full_src):
                z.write(full_src, arcname)
                print(f"Added to pack: {arcname}")
            else:
                print(f"Warning: File not found: {full_src}")
                
    print(f"\nDelivery package successfully created at: {output_zip}")
    print(f"Size: {os.path.getsize(output_zip) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    package_delivery()
