"""
video_assembler.py
Assembles final video: background + audio + text overlay.
Uses MoviePy + FFmpeg — both FREE and open source.

Install: pip install moviepy
"""

import subprocess
import os


def assemble_video(bg_video_path: str, audio_path: str, output_path: str) -> str:
    """
    Combine background video with audio track using FFmpeg.

    If the background video is shorter than the audio,
    it loops the video to match audio length.

    Args:
        bg_video_path: Background fruit character video/image
        audio_path: Tagalog MP3 audio
        output_path: Output video file path

    Returns:
        Path to assembled video
    """
    print(f"  🎬 Assembling video...")

    if not os.path.exists(bg_video_path):
        print(f"  ⚠️  Background video not found: {bg_video_path}")
        print(f"  ℹ️  Creating a simple colored background instead...")
        return create_fallback_video(audio_path, output_path)

    # Get audio duration
    audio_duration = get_media_duration(audio_path)
    print(f"  ⏱️  Audio duration: {audio_duration:.1f}s")

    # FFmpeg: loop background video, overlay with audio, 9:16 aspect ratio
    cmd = [
        "ffmpeg",
        "-stream_loop", "-1",       # loop video infinitely
        "-i", bg_video_path,        # background video input
        "-i", audio_path,           # audio input
        "-t", str(audio_duration),  # stop at audio length
        "-vf", (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920"        # enforce 9:16 vertical format
        ),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-y",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode == 0:
        print(f"  ✅ Video assembled: {output_path}")
        return output_path
    else:
        print(f"  ❌ Assembly error: {result.stderr[-300:]}")
        print(f"  ℹ️  Trying fallback method...")
        return create_fallback_video(audio_path, output_path)


def create_fallback_video(audio_path: str, output_path: str) -> str:
    """
    Create a simple video with a colorful background when no video asset exists.
    Uses FFmpeg's lavfi (audio/video filter) — no external files needed.
    """
    print(f"  🎨 Creating gradient background video...")

    audio_duration = get_media_duration(audio_path)

    # Create a purple-to-orange gradient background (eye-catching for social media)
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", (
            f"color=c=0x6A0DAD:size=1080x1920:rate=30:duration={audio_duration}"
        ),
        "-i", audio_path,
        "-vf", (
            "drawtext=text='🍎 FRUIT STORY 🍎':"
            "fontcolor=white:fontsize=60:"
            "x=(w-text_w)/2:y=(h-text_h)/2:"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-y",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode == 0:
        print(f"  ✅ Fallback video created: {output_path}")
        return output_path
    else:
        # Simplest possible fallback — just color + audio
        simple_cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", f"color=c=purple:size=1080x1920:rate=30:duration={audio_duration}",
            "-i", audio_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            "-y",
            output_path
        ]
        subprocess.run(simple_cmd, capture_output=True, timeout=300)
        return output_path


def get_media_duration(file_path: str) -> float:
    """Get duration of audio/video file in seconds using FFprobe."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 30.0   # default 30 seconds


def add_intro_text(video_path: str, fruit_name: str, output_path: str) -> str:
    """
    Add a 2-second title intro text overlay at the start of the video.
    Shows the fruit character name at the beginning.
    """
    print(f"  🏷️  Adding intro title text...")

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", (
            f"drawtext=text='{fruit_name}':"
            "fontcolor=yellow:fontsize=72:"
            "x=(w-text_w)/2:y=100:"
            "enable='between(t,0,2)':"
            "box=1:boxcolor=black@0.5:boxborderw=10"
        ),
        "-c:a", "copy",
        "-y",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode == 0:
        return output_path
    else:
        # If overlay fails, just use original video
        import shutil
        shutil.copy(video_path, output_path)
        return output_path
