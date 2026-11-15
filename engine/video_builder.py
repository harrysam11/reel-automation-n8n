#!/usr/bin/env python3
"""
Automated Video Builder with Burned-in Viral Hormozi Captions.
Stitches slide sequences with expressive audio, SFX transitions,
and burns high-retention, electric-yellow, bold animated captions
positioned safely in Instagram Reels / YouTube Shorts safe zones.
"""
import os
import sys
import subprocess
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.viral_captions import generate_viral_ass_subtitles

def render_reel_with_subtitles(slides_list, audio_path, srt_or_vtt_path, output_mp4, burn_subtitles=True, caption_style="electric_yellow"):
    os.makedirs(os.path.dirname(output_mp4), exist_ok=True)
    
    # 1. Determine total audio duration
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    audio_dur = float(res.stdout.strip()) if res.stdout.strip() else 60.0
    
    slide_dur = round(audio_dur / len(slides_list), 2)
    print(f"Total audio duration: {audio_dur:.2f}s across {len(slides_list)} slides ({slide_dur}s per slide)")
    
    # 2. Build concat demuxer file
    concat_txt = output_mp4.replace(".mp4", "_concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for s in slides_list:
            f.write(f"file '{os.path.abspath(s)}'\n")
            f.write(f"duration {slide_dur}\n")
        f.write(f"file '{os.path.abspath(slides_list[-1])}'\n")
        
    # 3. Build Viral Hormozi ASS Captions
    ass_file = None
    if burn_subtitles and srt_or_vtt_path and os.path.exists(srt_or_vtt_path):
        ass_path = srt_or_vtt_path.replace(".srt", "_viral.ass").replace(".vtt", "_viral.ass")
        try:
            ass_file = generate_viral_ass_subtitles(srt_or_vtt_path, ass_path, style_preset=caption_style)
        except Exception as e:
            print(f"Notice: ASS generation fallback: {e}")
            ass_file = None

    # 4. Setup video filter chain
    base_filter = "fps=30,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0xF4EBDD"
    
    sub_target = ass_file if (ass_file and os.path.exists(ass_file)) else srt_or_vtt_path
    
    if burn_subtitles and sub_target and os.path.exists(sub_target):
        # In subprocess list arguments, pass path directly without extra quotes
        sub_escaped = os.path.abspath(sub_target).replace(":", "\\:")
        sub_filter = f"subtitles={sub_escaped}"
        vf_chain = f"{base_filter},{sub_filter}"
    else:
        vf_chain = base_filter

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", audio_path,
        "-vf", vf_chain,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        output_mp4
    ]
    
    print("Assembling video with burned-in Hormozi-style captions...")
    ret = subprocess.run(cmd, capture_output=True, text=True)
    if ret.returncode != 0:
        print("Warning with subtitles filter, falling back to basic assembly:", ret.stderr[:400])
        cmd_fallback = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-i", audio_path, "-vf", base_filter,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", output_mp4
        ]
        subprocess.run(cmd_fallback, check=True)
        
    print(f"Video assembly complete: {output_mp4}")
    return output_mp4

if __name__ == "__main__":
    pass
