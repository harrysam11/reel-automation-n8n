#!/usr/bin/env python3
"""
Automated Video Builder with Burned-in Subtitles & Captions.
Stitches slide sequence with audio and burns high-contrast subtitles
positioned safely for Instagram Reels / YouTube Shorts safe zones.
"""
import os
import sys
import subprocess
import glob

def render_reel_with_subtitles(slides_list, audio_path, srt_or_vtt_path, output_mp4, burn_subtitles=True):
    os.makedirs(os.path.dirname(output_mp4), exist_ok=True)
    
    # 1. Determine total audio duration
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    audio_dur = float(res.stdout.strip()) if res.stdout.strip() else 95.0
    
    # Calculate duration per slide evenly or proportionally
    slide_dur = round(audio_dur / len(slides_list), 2)
    print(f"Total audio duration: {audio_dur:.2f}s across {len(slides_list)} slides ({slide_dur}s per slide)")
    
    # 2. Build concat demuxer file
    concat_txt = output_mp4.replace(".mp4", "_concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for s in slides_list:
            f.write(f"file '{os.path.abspath(s)}'\n")
            f.write(f"duration {slide_dur}\n")
        # Repeat last slide
        f.write(f"file '{os.path.abspath(slides_list[-1])}'\n")
        
    # 3. Setup video filter chain
    base_filter = "fps=30,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0xF4EBDD"
    
    # Instagram Safe Area Subtitles (High contrast bold white text with black outline)
    if burn_subtitles and srt_or_vtt_path and os.path.exists(srt_or_vtt_path):
        sub_escaped = os.path.abspath(srt_or_vtt_path).replace(":", "\\:").replace("'", "\\'")
        # Style: FontSize=22, PrimaryColour=White (&H00FFFFFF), OutlineColour=Black (&H00000000), MarginV=240 (Safe area)
        sub_filter = (
            f"subtitles='{sub_escaped}':force_style="
            "'FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=3,Shadow=1,Alignment=2,MarginV=240'"
        )
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
    
    print("Assembling video with burned-in subtitles...")
    ret = subprocess.run(cmd, capture_output=True, text=True)
    if ret.returncode != 0:
        print("Warning with subtitles, trying fallback assembly without subtitle filter:", ret.stderr)
        cmd_fallback = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-i", audio_path, "-vf", base_filter,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", output_mp4
        ]
        subprocess.run(cmd_fallback, check=True)
        
    print(f"Video assembly complete: {output_mp4}")
    return output_mp4
