#!/usr/bin/env python3
"""
Finance Reel Factory - Automated Multi-Video Creation Platform.
Generates complete vertical finance reels with:
- Modular visual templates (Hook, Comparison, Alert, Stat, Tier List, Outro)
- Real Human Neural Voiceover (Hindi / English via edge-tts)
- Burned-in, high-contrast captions & subtitles
- Automatic packaging & Android download sync
"""
import os
import sys
import json
import argparse
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.templates import (
    template_hook, template_comparison, template_stat,
    template_alert, template_tier_list, template_outro
)
from engine.tts_engine import synthesize_reel_audio
from engine.video_builder import render_reel_with_subtitles

def build_reel(project_id, title, voice="hi-IN-MadhurNeural", burn_subtitles=True):
    proj_dir = os.path.join(BASE_DIR, "PROJECTS", project_id)
    slides_dir = os.path.join(proj_dir, "05_SLIDES")
    audio_dir = os.path.join(proj_dir, "03_AUDIO")
    sub_dir = os.path.join(proj_dir, "06_SUBTITLES")
    export_dir = os.path.join(proj_dir, "08_EXPORT")
    
    for d in [slides_dir, audio_dir, sub_dir, export_dir]:
        os.makedirs(d, exist_ok=True)
        
    print(f"\n========================================================")
    print(f" Building Automated Reel: {project_id}")
    print(f" Voice: {voice}")
    print(f"========================================================\n")
    
    # 1. Generate Modular Slide Templates
    print("[1/4] Generating visual slide deck with modular templates...")
    slides = []
    
    # Slide 1: Hook
    s1 = template_hook(
        "🚨 CRITICAL MONEY DECISION",
        f"{title}\nReality Check!",
        "Agar aap SIP ya FD kar rahe ho,\ntoh yeh 95 seconds\naapke hazaron bacha sakte hain!"
    )
    p1 = os.path.join(slides_dir, "slide-01.png")
    s1.save(p1)
    slides.append(p1)
    
    # Slide 2: Comparison (SIP vs FD)
    s2 = template_comparison(
        "HEAD-TO-HEAD SHOWDOWN",
        "SIP vs Fixed Deposit\nKaun Jeetega?",
        "Option A: Equity SIP",
        [("Monthly Entry", "₹500 / month"), ("Historical CAGR", "12% – 14%"), ("Risk Level", "Market Volatile")],
        "Option B: Bank FD",
        [("Guaranteed Rate", "6.5% – 7.2%"), ("TDS Deduction", "Marginal Slab Rate"), ("Inflation Risk", "High Capital Erosion")]
    )
    p2 = os.path.join(slides_dir, "slide-02.png")
    s2.save(p2)
    slides.append(p2)
    
    # Slide 3: Stat & Calculation Trap
    s3 = template_stat(
        "SHOCKING TAX TRAP",
        "Fixed Deposit Math\nReal Return Revealed",
        "NEGATIVE REAL RETURN",
        "After 30% Tax Slab & 6% CPI Inflation",
        [
            ("1. Nominal Bank FD Rate", "+ 7.00%"),
            ("2. Tax Deduction (30% Slab)", "- 2.10%"),
            ("3. Net In-Hand Return", "= 4.90%"),
            ("4. Actual Inflation", "- 5.80%"),
            ("5. NET REAL PURCHASING POWER", "= -0.90% LOSS")
        ],
        accent_color=(220, 38, 38)
    )
    p3 = os.path.join(slides_dir, "slide-03.png")
    s3.save(p3)
    slides.append(p3)
    
    # Slide 4: Alert / Reality Check
    s4 = template_alert(
        "BANK INSURANCE LIMIT",
        "DICGC Reality Check\nKitna Paisa Safe Hai?",
        "MAXIMUM COVER: ₹5,00,000",
        "Chahe bank account me ₹50 Lakh hon...\nBank default hone par kanoon ke mutabik\nsirf ₹5 Lakh (Principal + Byaj) protected hain!\n\nPaisa multiple scheduled banks me diversify karein!"
    )
    p4 = os.path.join(slides_dir, "slide-04.png")
    s4.save(p4)
    slides.append(p4)
    
    # Slide 5: Tier List Capital Blueprint
    s5 = template_tier_list(
        "INVESTMENT BLUEPRINT",
        "Tier 1: Small Capital Map\nEntry: ₹100 – ₹5,000",
        "ACCESSIBLE ENTRY BRACKET",
        (22, 163, 74),
        [
            ("1. Mutual Funds", "₹100 – ₹500", "Micro SIPs on broad index"),
            ("2. ETFs (NiftyBeES)", "~₹250", "1 unit traded on exchange"),
            ("3. Direct Stocks", "₹10 – ₹5,000+", "Single share on NSE/BSE"),
            ("4. PPF / SSY", "₹250 – ₹500/yr", "Guaranteed Sovereign backing"),
            ("5. NPS Tier-1", "₹500 – ₹1,000", "Retirement tax deduction"),
            ("6. Bank FDs / RDs", "₹100 – ₹1,000", "Emergency liquid reserve")
        ]
    )
    p5 = os.path.join(slides_dir, "slide-05.png")
    s5.save(p5)
    slides.append(p5)
    
    # Slide 6: Outro & Next Reels
    s6 = template_outro(
        "BECOME FINANCIALLY SMART",
        "Follow for Daily\nFinance Reality Checks!",
        "👉 TAP FOLLOW",
        [
            "SIP vs Lump Sum in 2026",
            "FD vs Debt Funds Tax Showdown",
            "Savings Account Inflation Leak",
            "Where to Invest Your First ₹1,000"
        ],
        "Disclaimer: For educational purposes only.\nSecurities investments are subject to market risks.\nNot SEBI registered investment advice."
    )
    p6 = os.path.join(slides_dir, "slide-06.png")
    s6.save(p6)
    slides.append(p6)
    
    # 2. Synthesize Real Neural Voice & Generate Subtitles
    print("\n[2/4] Generating natural neural voiceover + subtitle captions...")
    script_file = os.path.join(proj_dir, "02_SCRIPT", "voiceover_clean.txt")
    if os.path.exists(script_file):
        with open(script_file, "r", encoding="utf-8") as f:
            full_text = " ".join([line.strip() for line in f if line.strip()])
    else:
        full_text = (
            "अगर आप SIP या FD कर रहे हो, तो ये बात ध्यान से सुनिए! "
            "SIP में आप हर महीने सिर्फ पांच सौ रुपये से देश की टॉप कंपनियों में हिस्सेदार बनते हैं। "
            "लेकिन FD में टैक्स और इन्फ्लेशन के बाद आपका रियल रिटर्न लगभग नेगेटिव हो जाता है! "
            "और बैंक डूबने पर DICGC सिर्फ पांच लाख रुपये तक ही इंश्योर्ड करता है। "
            "इसलिए समझदारी से इन्वेस्ट करें और अभी Follow बटन दबाइए!"
        )
        
    audio_path = os.path.join(audio_dir, "voiceover.mp3")
    srt_path = os.path.join(sub_dir, "captions.vtt")
    
    # Synthesize with real human voice
    cmd_edge = [
        sys.executable, "-m", "edge_tts",
        "--voice", voice,
        "--text", full_text,
        "--write-media", audio_path,
        "--write-subtitles", srt_path
    ]
    res_tts = subprocess.run(cmd_edge, capture_output=True, text=True)
    if res_tts.returncode != 0:
        print("Notice: CLI edge-tts fallback, running engine synthesizer...")
        synthesize_reel_audio(full_text, audio_path, srt_path, voice_key=voice)
        
    # Also save as WAV for editing
    audio_wav = os.path.join(audio_dir, "voiceover.wav")
    subprocess.run(["ffmpeg", "-y", "-i", audio_path, audio_wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Assemble Vertical Video with Burned-in Subtitles
    print("\n[3/4] Assembling 1080x1920 MP4 video with burned-in subtitles...")
    out_mp4 = os.path.join(export_dir, "reel_final.mp4")
    render_reel_with_subtitles(slides, audio_path, srt_path, out_mp4, burn_subtitles=burn_subtitles)
    
    # 4. Package Delivery
    print("\n[4/4] Creating delivery pack...")
    zip_path = os.path.join(BASE_DIR, "OUTPUTS", f"{project_id}_DELIVERY_PACK.zip")
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    import zipfile
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(out_mp4, "video/reel_final.mp4")
        z.write(audio_path, "audio/voiceover.mp3")
        if os.path.exists(srt_path):
            z.write(srt_path, "subtitles/captions.vtt")
        for s in slides:
            z.write(s, f"slides/{os.path.basename(s)}")
            
    print(f"\n========================================================")
    print(f" REEL GENERATION COMPLETE!")
    print(f" Video Output: {out_mp4}")
    print(f" Package Zip : {zip_path}")
    print(f"========================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finance Reel Factory Automated Platform")
    parser.add_argument("--project", default="REEL_001_SIP_FD_REALITY_CHECK", help="Project ID")
    parser.add_argument("--title", default="SIP & FD Users", help="Reel Title")
    parser.add_argument("--voice", default="hi-IN-MadhurNeural", help="Voice (hi-IN-MadhurNeural, hi-IN-SwaraNeural, en-IN-PrabhatNeural)")
    parser.add_argument("--no-subtitles", action="store_true", help="Disable burned-in subtitles")
    args = parser.parse_args()
    
    build_reel(args.project, args.title, voice=args.voice, burn_subtitles=not args.no_subtitles)
