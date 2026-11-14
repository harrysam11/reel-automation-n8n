# wmill: python3
"""
Windmill script to generate Hindi/English offline narration using Kokoro-82M TTS.
"""
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.tts_generator import generate_reel_voiceover

def main(
    project_id: str = "REEL_001_SIP_FD_REALITY_CHECK",
    voice: str = "hm_omega",
    speed: float = 1.05
) -> dict:
    script_path = os.path.join(REPO_ROOT, "PROJECTS", project_id, "02_SCRIPT", "voiceover_clean.txt")
    wav_path = os.path.join(REPO_ROOT, "PROJECTS", project_id, "03_AUDIO", "voiceover.wav")
    
    duration = generate_reel_voiceover(script_path, wav_path, voice=voice, speed=speed)
    return {
        "success": True,
        "project_id": project_id,
        "voice": voice,
        "speed": speed,
        "duration_sec": round(duration, 2),
        "wav_path": wav_path
    }
