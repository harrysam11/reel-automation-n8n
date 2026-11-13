#!/usr/bin/env python3
"""
Kokoro TTS Benchmark Suite for Finance Reel Factory.
Tests:
1. Pure Hindi (Devanagari)
2. Pure English (Financial terminology)
3. Hinglish (Mixed Devanagari + Latin finance terms)

Measures:
- Generation Speed (seconds & Real-Time Factor)
- Output Duration (seconds)
- Memory Footprint (Resident Set Size)
"""
import os
import time
import resource
import soundfile as sf
from kokoro_onnx import Kokoro

MODEL_PATH = "models/kokoro-v1.0.onnx"
VOICES_PATH = "models/voices-v1.0.bin"
BENCH_DIR = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/03_AUDIO/bench"

TEST_CASES = [
    {
        "name": "Hindi (Devanagari)",
        "lang": "hi",
        "voice": "hm_omega",  # Hindi Male
        "text": "अगर आप एसआईपी या एफडी कर रहे हैं, तो यह बात ध्यान से सुनिए। हर महीने थोड़ी सी बचत आपके भविष्य को सुरक्षित कर सकती है।"
    },
    {
        "name": "English (Financial)",
        "lang": "en-us",
        "voice": "am_adam",   # English Male
        "text": "Systematic Investment Plans offer rupee cost averaging across mutual fund portfolios, while fixed deposits provide nominal safety under central bank guidelines."
    },
    {
        "name": "Hinglish (Mixed)",
        "lang": "hi",
        "voice": "hm_psi",    # Hindi Male alternative
        "text": "अगर आप SIP या FD कर रहे हो, तो ध्यान रहे—bank default hone par DICGC ke तहत sirf 5 lakh tak hi insured hote hain!"
    }
]

def run_benchmark():
    os.makedirs(BENCH_DIR, exist_ok=True)
    
    print("=" * 65)
    print("      KOKORO-82M TTS CPU BENCHMARK (i3-10100 Workstation)      ")
    print("=" * 65)
    
    # 1. Initialize engine
    init_start = time.perf_counter()
    kokoro = Kokoro(MODEL_PATH, VOICES_PATH)
    init_time = time.perf_counter() - init_start
    print(f"Model initialization time: {init_time:.2f}s")
    
    results = []
    
    for tc in TEST_CASES:
        name = tc["name"]
        voice = tc["voice"]
        text = tc["text"]
        lang = tc["lang"]
        
        print(f"\n--- Testing: {name} (Voice: {voice}, Lang: {lang}) ---")
        print(f"Text: \"{text}\"")
        
        # Warmup / inference timing
        t0 = time.perf_counter()
        samples, sample_rate = kokoro.create(
            text,
            voice=voice,
            speed=1.0,
            lang=lang
        )
        t_gen = time.perf_counter() - t0
        
        audio_dur = len(samples) / sample_rate
        rtf = t_gen / audio_dur if audio_dur > 0 else 0
        
        # Output file
        out_filename = f"{name.lower().split()[0]}_{voice}.wav"
        out_path = os.path.join(BENCH_DIR, out_filename)
        sf.write(out_path, samples, sample_rate)
        
        # Memory measurement
        rss_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss_mb = rss_kb / 1024.0
        
        res_info = {
            "name": name,
            "voice": voice,
            "gen_time_sec": round(t_gen, 3),
            "audio_dur_sec": round(audio_dur, 2),
            "rtf": round(rtf, 3),
            "rss_mb": round(rss_mb, 1),
            "file": out_path
        }
        results.append(res_info)
        
        print(f"Generated Audio : {audio_dur:.2f}s")
        print(f"Generation Time : {t_gen:.2f}s (RTF: {rtf:.2f}x - {1/rtf:.1f}x real-time)")
        print(f"Saved To        : {out_path}")
        
    print("\n" + "=" * 65)
    print(f"{'Test Case':<22} | {'Voice':<10} | {'Gen (s)':<8} | {'Dur (s)':<8} | {'RTF':<6} | {'RAM (MB)':<8}")
    print("-" * 65)
    for r in results:
        print(f"{r['name']:<22} | {r['voice']:<10} | {r['gen_time_sec']:<8} | {r['audio_dur_sec']:<8} | {r['rtf']:<6} | {r['rss_mb']:<8}")
    print("=" * 65)

if __name__ == "__main__":
    run_benchmark()
