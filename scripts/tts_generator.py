#!/usr/bin/env python3
"""
Kokoro TTS Voiceover Generator for Finance Reel Factory.
Generates full reel narration from voiceover_clean.txt using Kokoro-82M ONNX engine.
Automatically inserts natural pauses between scenes and outputs WAV + MP3.
"""
import os
import sys
import subprocess
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

MODEL_PATH = os.getenv("KOKORO_MODEL_PATH", "models/kokoro-v1.0.onnx")
VOICES_PATH = os.getenv("KOKORO_VOICES_PATH", "models/voices-v1.0.bin")
DEFAULT_VOICE = os.getenv("DEFAULT_NARRATOR_VOICE", "hm_omega")
DEFAULT_SPEED = float(os.getenv("DEFAULT_SPEECH_SPEED", "1.05"))

def generate_reel_voiceover(script_path, output_wav, voice=None, speed=None):
    voice = voice or DEFAULT_VOICE
    speed = speed if speed is not None else DEFAULT_SPEED
    os.makedirs(os.path.dirname(output_wav), exist_ok=True)
    
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VOICES_PATH):
        raise FileNotFoundError(f"Kokoro model files missing: {MODEL_PATH}")
        
    print(f"Loading Kokoro engine (voice: {voice}, speed: {speed})...")
    kokoro = Kokoro(MODEL_PATH, VOICES_PATH)
    
    with open(script_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
        
    print(f"Synthesizing {len(lines)} narrative segments...")
    combined_audio = []
    sample_rate = 24000
    
    # 0.4s pause between segments
    pause_samples = np.zeros(int(0.4 * sample_rate), dtype=np.float32)
    
    for idx, line in enumerate(lines):
        print(f"  [{idx+1}/{len(lines)}] {line[:40]}...")
        # Use Hindi tokenizer/phonemizer
        samples, sr = kokoro.create(line, voice=voice, speed=speed, lang="hi")
        sample_rate = sr
        combined_audio.append(samples)
        if idx < len(lines) - 1:
            combined_audio.append(pause_samples)
            
    final_waveform = np.concatenate(combined_audio)
    total_dur = len(final_waveform) / sample_rate
    
    sf.write(output_wav, final_waveform, sample_rate)
    print(f"\nFinal narration written: {output_wav}")
    print(f"Total duration: {total_dur:.2f} seconds")
    
    # Generate MP3 preview for Android
    preview_mp3 = output_wav.replace(".wav", "_preview.mp3")
    cmd = [
        "ffmpeg", "-y", "-i", output_wav,
        "-codec:a", "libmp3lame", "-b:a", "128k",
        preview_mp3
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Preview MP3 generated: {preview_mp3}")
    return total_dur

if __name__ == "__main__":
    script = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/02_SCRIPT/voiceover_clean.txt"
    wav = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/03_AUDIO/voiceover.wav"
    generate_reel_voiceover(script, wav)
