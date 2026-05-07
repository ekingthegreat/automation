"""
🍎 AI FRUIT STORY BOT — Main Pipeline
Automatically generates Tagalog fruit stories, adds captions,
and schedules upload to YouTube and TikTok.

Run: python main.py
"""

import os
import time
import json
import subprocess
from datetime import datetime

from story_generator import generate_tagalog_story
from tts_generator import generate_tagalog_audio
from caption_generator import generate_captions, burn_captions
from video_assembler import assemble_video
from uploader import upload_to_youtube, schedule_tiktok

# ──────────────────────────────────────────────
# CONFIG — edit these values
# ──────────────────────────────────────────────
CONFIG = {
    "fruit_characters": [
        "Mangga (Mango)", "Saging (Banana)", "Mansanas (Apple)",
        "Pakwan (Watermelon)", "Pinya (Pineapple)", "Ubas (Grapes)"
    ],
    "story_themes": [
        "pagmamahal", "pagsasakripisyo", "katapangan",
        "pagkakaibigan", "tagumpay", "selos"
    ],
    "output_folder": "output_videos",
    "watermark_text": "FruitStoriesPH",
    "video_format": "9:16",       # vertical for TikTok/Shorts
    "video_duration_sec": 30,
    "youtube_channel": "YOUR_YOUTUBE_CHANNEL",
    "tiktok_account": "YOUR_TIKTOK_ACCOUNT",
}

def run_pipeline():
    """Run the full pipeline: story → audio → captions → video → upload"""

    print("\n" + "="*50)
    print("  🍎 FRUIT STORY BOT STARTING...")
    print("="*50 + "\n")

    # Create output folder
    os.makedirs(CONFIG["output_folder"], exist_ok=True)

    # Pick random fruit and theme
    import random
    fruit = random.choice(CONFIG["fruit_characters"])
    theme = random.choice(CONFIG["story_themes"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"🍑 Character : {fruit}")
    print(f"📖 Theme     : {theme}")
    print(f"🕐 Timestamp : {timestamp}\n")

    # ── STEP 1: Generate Tagalog Story ──────────
    print("STEP 1: Generating Tagalog story...")
    story_data = generate_tagalog_story(fruit, theme)
    story_file = f"{CONFIG['output_folder']}/story_{timestamp}.json"
    with open(story_file, "w", encoding="utf-8") as f:
        json.dump(story_data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Story saved: {story_file}")
    print(f"  📝 Title: {story_data['title']}\n")

    # ── STEP 2: Text-to-Speech (Tagalog) ────────
    print("STEP 2: Generating Tagalog audio...")
    audio_file = f"{CONFIG['output_folder']}/audio_{timestamp}.mp3"
    generate_tagalog_audio(story_data["story_text"], audio_file)
    print(f"  ✅ Audio saved: {audio_file}\n")

    # ── STEP 3: Generate Captions ────────────────
    print("STEP 3: Generating captions with Whisper...")
    srt_file = f"{CONFIG['output_folder']}/captions_{timestamp}.srt"
    generate_captions(audio_file, srt_file)
    print(f"  ✅ Captions saved: {srt_file}\n")

    # ── STEP 4: Assemble Final Video ─────────────
    print("STEP 4: Assembling video...")
    # You can put your fruit character image/video here
    bg_video = "assets/fruit_background.mp4"   # your background clip
    raw_video = f"{CONFIG['output_folder']}/raw_{timestamp}.mp4"
    final_video = f"{CONFIG['output_folder']}/final_{timestamp}.mp4"

    assemble_video(bg_video, audio_file, raw_video)
    burn_captions(raw_video, srt_file, final_video)
    print(f"  ✅ Final video: {final_video}\n")

    # ── STEP 5: Upload ────────────────────────────
    print("STEP 5: Uploading to platforms...")

    title = story_data["title"]
    description = story_data["description"]
    tags = story_data["tags"]

    upload_to_youtube(final_video, title, description, tags)
    schedule_tiktok(final_video, title)

    print("\n" + "="*50)
    print("  ✅ PIPELINE COMPLETE!")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_pipeline()
