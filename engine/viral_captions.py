#!/usr/bin/env python3
"""
Viral Hormozi-Style Captions Generator for Finance Reel Factory.
Converts boring sentence subtitles into high-retention, fast-paced (1-3 words)
bold captions with electric yellow highlights, thick black outlines, and viral emojis.
"""
import os
import re

EMOJI_KEYWORDS = {
    r"\b(sip|mutual fund|cagr|compounding)\b": "📈",
    r"\b(fd|fixed deposit|bank)\b": "🏦",
    r"\b(tax|taxation|30%)\b": "💸",
    r"\b(risk|loss|crash|down)\b": "💥",
    r"\b(safe|security|insured|dicgc)\b": "🛡️",
    r"\b(rupees?|₹|crore|lakh|money|paisa|paisa|saving)\b": "💰",
    r"\b(alert|stop|critical|dhyan)\b": "🚨",
    r"\b(gold|sgb)\b": "🪙",
    r"\b(follow|subscribe)\b": "👉",
}

def parse_srt(srt_content):
    """Parse SRT into a list of subtitle items: [{start, end, text}]."""
    entries = []
    blocks = re.split(r"\n\s*\n", srt_content.strip())
    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if len(lines) >= 3:
            time_match = re.match(r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})", lines[1])
            if time_match:
                start_str, end_str = time_match.group(1), time_match.group(2)
                text = " ".join(lines[2:])
                entries.append({
                    "start": srt_to_seconds(start_str),
                    "end": srt_to_seconds(end_str),
                    "text": text
                })
    return entries

def srt_to_seconds(time_str):
    time_str = time_str.replace(",", ".")
    parts = time_str.split(":")
    hours = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def seconds_to_ass_time(sec):
    hours = int(sec // 3600)
    minutes = int((sec % 3600) // 60)
    secs = int(sec % 60)
    centis = int(round((sec - int(sec)) * 100))
    if centis >= 100:
        secs += 1
        centis = 0
    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"

def add_viral_emojis(text):
    """Attach context-aware financial emojis to power words."""
    result = text
    lower = text.lower()
    for pattern, emoji in EMOJI_KEYWORDS.items():
        if re.search(pattern, lower):
            result = f"{result} {emoji}"
            break
    return result

def convert_to_viral_chunks(entries, max_words_per_cue=2):
    """
    Splits long sentence cues into high-energy 1 to 2 word rapid bursts.
    """
    viral_cues = []
    for entry in entries:
        words = entry["text"].split()
        if not words:
            continue
        total_dur = max(0.4, entry["end"] - entry["start"])
        word_dur = total_dur / len(words)
        
        # Group into chunks
        chunks = []
        for i in range(0, len(words), max_words_per_cue):
            chunk_words = words[i:i + max_words_per_cue]
            chunk_text = " ".join(chunk_words).upper()
            chunk_text = add_viral_emojis(chunk_text)
            c_start = entry["start"] + i * word_dur
            c_end = min(entry["end"], entry["start"] + (i + len(chunk_words)) * word_dur)
            chunks.append({
                "start": c_start,
                "end": c_end,
                "text": chunk_text
            })
        viral_cues.extend(chunks)
    return viral_cues

def generate_viral_ass_subtitles(srt_path, output_ass_path, style_preset="electric_yellow"):
    """
    Builds an Advanced SubStation Alpha (.ass) subtitle file formatted
    with Alex Hormozi / MrBeast viral styling for 1080x1920 Instagram Reels.
    """
    if not os.path.exists(srt_path):
        return None
        
    with open(srt_path, "r", encoding="utf-8") as f:
        srt_content = f.read()
        
    entries = parse_srt(srt_content)
    if not entries:
        return None
        
    viral_cues = convert_to_viral_chunks(entries, max_words_per_cue=2)
    
    # Styles:
    # ASS Color format: &HAABBGGRR (Alpha, Blue, Green, Red)
    if style_preset == "neon_green":
        primary_color = "&H0033FF33"  # Neon Green
    elif style_preset == "punchy_white":
        primary_color = "&H00FFFFFF"  # Crisp White
    else:  # electric_yellow (default Hormozi)
        primary_color = "&H0000FFFF"  # Electric Yellow
        
    outline_color = "&H00000000"  # Heavy Deep Black Outline
    back_color = "&H80000000"     # Drop Shadow
    
    ass_header = f"""[Script Info]
Title: Viral Reel Hormozi Captions
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HormoziViral,Noto Sans,46,{primary_color},&H000000FF,{outline_color},{back_color},-1,0,0,0,100,100,0,0,1,6,3,2,60,60,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    dialogues = []
    for cue in viral_cues:
        start_t = seconds_to_ass_time(cue["start"])
        end_t = seconds_to_ass_time(cue["end"])
        text = cue["text"]
        # Add slight bold pop
        formatted_text = "{\\b1}" + text + "{\\b0}"
        dialogues.append(f"Dialogue: 0,{start_t},{end_t},HormoziViral,,0,0,0,,{formatted_text}")
        
    os.makedirs(os.path.dirname(output_ass_path), exist_ok=True)
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(dialogues) + "\n")
        
    print(f"Generated Viral Hormozi ASS Captions: {output_ass_path} ({len(viral_cues)} cues)")
    return output_ass_path

if __name__ == "__main__":
    import sys
    test_srt = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/03_AUDIO/voiceover.srt"
    test_ass = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/03_AUDIO/viral_captions.ass"
    if os.path.exists(test_srt):
        generate_viral_ass_subtitles(test_srt, test_ass)
