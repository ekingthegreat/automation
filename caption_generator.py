"""
caption_generator.py
Auto-generates Tagalog subtitles from audio using OpenAI Whisper (FREE).
Burns captions into video using FFmpeg (FREE).

Install:
  pip install openai-whisper
  Download FFmpeg: https://ffmpeg.org/download.html
"""

import whisper
import subprocess
import os
import re


def generate_captions(audio_path: str, srt_output_path: str) -> str:
    """
    Transcribe audio to SRT subtitle file using Whisper.

    Args:
        audio_path: Path to MP3/WAV audio file
        srt_output_path: Where to save the .srt file

    Returns:
        Path to the SRT file
    """
    print(f"  🎧 Loading Whisper model (base)...")
    # 'base' model is free and fast. Use 'small' for better accuracy.
    # Models: tiny, base, small, medium, large (larger = slower but more accurate)
    model = whisper.load_model("base")

    print(f"  📝 Transcribing audio: {audio_path}")
    result = model.transcribe(
        audio_path,
        language="tl",          # Tagalog language code
        task="transcribe",
        word_timestamps=True,    # Enable word-level timing
    )

    # Build SRT content
    srt_content = build_srt(result["segments"])

    with open(srt_output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

    print(f"  ✅ Captions saved: {srt_output_path}")
    print(f"  📊 Total segments: {len(result['segments'])}")
    return srt_output_path


def build_srt(segments: list) -> str:
    """
    Convert Whisper segments to SRT format.

    Args:
        segments: List of Whisper transcription segments

    Returns:
        SRT formatted string
    """
    srt_lines = []

    for i, segment in enumerate(segments, start=1):
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip()

        # Clean up text
        text = clean_caption_text(text)

        if text:
            srt_lines.append(f"{i}")
            srt_lines.append(f"{start} --> {end}")
            srt_lines.append(text)
            srt_lines.append("")   # blank line between entries

    return "\n".join(srt_lines)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def clean_caption_text(text: str) -> str:
    """Clean and format caption text for readability."""
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]
    return text


def burn_captions(video_path: str, srt_path: str, output_path: str) -> str:
    """
    Burn SRT captions into video using FFmpeg.
    Captions are styled: white bold text with dark outline — great for mobile.

    Args:
        video_path: Input video file
        srt_path: Path to .srt captions file
        output_path: Output video with burnt-in captions

    Returns:
        Path to output video
    """
    print(f"  🖊️  Burning captions into video...")

    # Caption style: white bold text, black outline, bottom center
    # Adjust FontSize (24-32 works well for 9:16 vertical videos)
    subtitle_style = (
        "FontName=Arial Black,"
        "FontSize=36,"
        "PrimaryColour=&H0000FFFF,"   # yellow text
        "SecondaryColour=&H00FFFFFF," # white for secondary words
        "OutlineColour=&H00000000,"   # black outline
        "BackColour=&H00000000,"
        "BorderStyle=1,"
        "Outline=3,"
        "Shadow=0,"
        "Bold=1,"
        "Alignment=2,"                # bottom center
        "MarginV=60"
    )

    # Escape path for FFmpeg (handle spaces and special chars)
    srt_escaped = srt_path.replace("\\", "/").replace(":", "\\:")

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles='{srt_escaped}':force_style='{subtitle_style}'",
        "-c:a", "copy",
        "-y",             # overwrite output if exists
        output_path
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  ✅ Video with captions saved ({size_mb:.1f} MB): {output_path}")
            return output_path
        else:
            print(f"  ❌ FFmpeg error:\n{result.stderr[-500:]}")
            raise Exception("FFmpeg caption burning failed")

    except subprocess.TimeoutExpired:
        print("  ❌ FFmpeg timed out")
        raise
    except FileNotFoundError:
        print("  ❌ FFmpeg not found! Please install FFmpeg:")
        print("     Windows: https://ffmpeg.org/download.html")
        print("     Mac: brew install ffmpeg")
        print("     Linux: sudo apt install ffmpeg")
        raise
