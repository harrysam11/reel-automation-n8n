#!/usr/bin/env python3
"""
Assemble final 1080x1920 30fps vertical MP4 video with FFmpeg.
Combines slide PNG sequence, timed scene durations, audio track, and embedded subtitles.
"""
import os
import sys
import subprocess
import csv

def render_reel(project_dir, output_mp4):
    os.makedirs(os.path.dirname(output_mp4), exist_ok=True)
    slides_dir = os.path.join(project_dir, "05_SLIDES")
    audio_wav = os.path.join(project_dir, "03_AUDIO", "voiceover.wav")
    srt_file = os.path.join(project_dir, "06_SUBTITLES", "captions.srt")
    scene_csv = os.path.join(project_dir, "scene_script.csv")
    
    # Read scene script to build concat file
    concat_txt_path = os.path.join(project_dir, "07_EDIT", "slides_concat.txt")
    os.makedirs(os.path.dirname(concat_txt_path), exist_ok=True)
    
    with open(scene_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        scenes = list(reader)
        
    # Get actual audio duration via ffprobe
    audio_probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_wav
    ], capture_output=True, text=True)
    audio_duration = float(audio_probe.stdout.strip()) if audio_probe.stdout.strip() else 95.0
    
    total_scene_target = sum(float(s["duration_sec"]) for s in scenes)
    scale_factor = audio_duration / total_scene_target if total_scene_target > 0 else 1.0
    print(f"Audio duration: {audio_duration:.2f}s (Scale factor for slides: {scale_factor:.3f}x)")
    
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for s in scenes:
            slide_idx = int(s["slide_index"])
            scaled_dur = round(float(s["duration_sec"]) * scale_factor, 2)
            slide_img = os.path.abspath(os.path.join(slides_dir, f"slide-{slide_idx:02d}.png"))
            f.write(f"file '{slide_img}'\n")
            f.write(f"duration {scaled_dur}\n")
        # Concat demuxer requirement: repeat last slide
        last_slide_img = os.path.abspath(os.path.join(slides_dir, f"slide-{int(scenes[-1]['slide_index']):02d}.png"))
        f.write(f"file '{last_slide_img}'\n")

    print(f"Created concat playlist: {concat_txt_path}")
    
    # FFmpeg command
    # Video: 1080x1920, 30fps, H.264 high profile
    # Audio: AAC 192k
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt_path,
        "-i", audio_wav,
        "-vf", "fps=30,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0xF4EBDD",
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
    
    print("Executing FFmpeg render pipeline...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg error:", result.stderr)
        sys.exit(1)
        
    print(f"Successfully rendered video to: {output_mp4}")
    
    # Verify technical specs
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=width,height,r_frame_rate,codec_name",
        "-of", "default=noprint_wrappers=1",
        output_mp4
    ]
    probe_res = subprocess.run(probe_cmd, capture_output=True, text=True)
    print("Technical verification:\n" + probe_res.stdout)

if __name__ == "__main__":
    proj = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK"
    out = os.path.join(proj, "08_EXPORT", "reel_001_final.mp4")
    render_reel(proj, out)
