# 🍎 AI Fruit Story Bot
### Automatic Tagalog Fruit Story Generator for YouTube & TikTok
#### 100% FREE Stack — ₱0/month

---

## 📋 What This Does

1. **Generates** a Tagalog fruit character story (using local AI or templates)
2. **Converts** the story to Tagalog speech (Google TTS — free)
3. **Auto-generates** Tagalog captions (OpenAI Whisper — free)
4. **Assembles** the final video (FFmpeg — free)
5. **Uploads** to YouTube and TikTok automatically (free APIs)
6. **Runs daily** on a schedule without you doing anything

---

## 🖥️ REQUIREMENTS

- **Python 3.9+** (free): https://python.org
- **FFmpeg** (free): https://ffmpeg.org
- **8GB RAM** recommended (for Whisper AI)
- Internet connection (for gTTS and uploads)

---

## 🚀 STEP-BY-STEP SETUP

### STEP 1 — Install Python
1. Go to https://python.org/downloads
2. Download Python 3.11 (latest)
3. Install it — **check "Add to PATH"** during install
4. Verify: open Command Prompt/Terminal and type:
   ```
   python --version
   ```

---

### STEP 2 — Install FFmpeg

**Windows:**
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Download `ffmpeg-release-essentials.zip`
3. Extract to `C:\ffmpeg\`
4. Add `C:\ffmpeg\bin` to your System PATH:
   - Search "Environment Variables" in Windows
   - Edit PATH → Add `C:\ffmpeg\bin`
5. Verify: `ffmpeg -version`

**Mac:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

---

### STEP 3 — Download This Project
```bash
# Create a project folder
mkdir fruit_story_bot
cd fruit_story_bot

# Copy all .py files into this folder
```

---

### STEP 4 — Install Python Packages
```bash
pip install -r requirements.txt
```

This installs everything for free:
- `gtts` — Tagalog text-to-speech
- `openai-whisper` — Auto captions
- `moviepy` — Video editing
- `google-api-python-client` — YouTube upload
- `schedule` — Auto daily posting

---

### STEP 5 — (Optional) Install Ollama for Better Stories

Ollama runs a FREE local AI on your PC for better Tagalog stories:

1. Download from: https://ollama.ai
2. Install and run
3. Open a new terminal and run:
   ```bash
   ollama pull llama3
   ```
4. That's it! The bot will automatically use it.

---

### STEP 6 — Set Up YouTube API (Free)

1. Go to: https://console.cloud.google.com
2. Create a new project (name it "FruitStoryBot")
3. Go to **APIs & Services** → **Enable APIs**
4. Search for **"YouTube Data API v3"** → Enable it
5. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
6. Choose **Desktop App** → Create
7. Download the JSON file
8. **Rename it to `client_secrets.json`**
9. Place it in your `fruit_story_bot` folder

First time you run the bot, a browser window will open asking you to log in with your Google account. After that, it saves the token and never asks again.

---

### STEP 7 — Set Up TikTok API (Free)

**Option A: Use TikTok's Native Free Scheduler (Easiest)**
1. Go to: https://tiktok.com/creator-center
2. Click "Upload" → Set your scheduled time
3. No code needed — just manually upload when the bot creates the video

**Option B: Use TikTok Content Posting API (Full Automation)**
1. Go to: https://developers.tiktok.com
2. Create a developer account (free)
3. Create a new app
4. Request access to "Content Posting API"
5. After approval, get your Access Token
6. Create a `.env` file in your project folder:
   ```
   TIKTOK_ACCESS_TOKEN=your_token_here
   ```

---

### STEP 8 — Add Your Fruit Background Video

Place a fruit character video in:
```
fruit_story_bot/
  assets/
    fruit_background.mp4   ← put your video here
```

**Where to get free fruit character videos:**
- Download from: https://media.io (free tier)
- Download from: https://ninjachat.ai/fruit-love-island (free)
- Download from: https://aifruit.net (3 free/day)

If you don't add a video, the bot will create a simple colored background automatically.

---

### STEP 9 — Run the Bot!

**Test once:**
```bash
python main.py
```

**Run on auto-schedule (daily):**
```bash
python scheduler.py
```

Keep this terminal open or run it in the background. The bot will post every day at 9 AM automatically.

---

## 📁 PROJECT STRUCTURE

```
fruit_story_bot/
├── main.py              ← Main pipeline (run this)
├── scheduler.py         ← Auto daily scheduler
├── story_generator.py   ← Tagalog story AI
├── tts_generator.py     ← Text to speech
├── caption_generator.py ← Auto captions (Whisper)
├── video_assembler.py   ← FFmpeg video builder
├── uploader.py          ← YouTube + TikTok upload
├── requirements.txt     ← Python packages
├── client_secrets.json  ← YouTube credentials (you add this)
├── .env                 ← TikTok token (you add this)
└── assets/
    └── fruit_background.mp4  ← Your fruit video (you add this)
```

---

## ⚙️ CUSTOMIZATION

Edit `main.py` → `CONFIG` section to change:

```python
CONFIG = {
    # Add more fruit characters
    "fruit_characters": ["Mangga", "Saging", "Mansanas", ...],

    # Change story themes
    "story_themes": ["pagmamahal", "katapangan", "selos", ...],

    # Change posting schedule in scheduler.py
    # Current: daily 9AM
}
```

---

## 🔧 TROUBLESHOOTING

| Problem | Solution |
|---|---|
| `ffmpeg not found` | Install FFmpeg and add to PATH |
| `gtts error` | Check internet connection |
| `whisper slow` | Normal — first run downloads model (~150MB) |
| `YouTube auth error` | Delete `youtube_token.pickle` and re-run |
| `TikTok 401 error` | Token expired — generate a new one |
| `No module named X` | Run `pip install -r requirements.txt` |

---

## 💡 TIPS FOR GOING VIRAL

1. **Post 1-2x daily** — consistency beats quality early on
2. **Use trending sounds** — add background music manually in TikTok app
3. **Best posting times (PH):** 7-9AM, 12-1PM, 7-10PM
4. **Hashtags:** #FruitStory #TagalogStory #AIFruit #PinoyContent #FruitDrama
5. **Engage with comments** — reply to grow faster

---

## 📊 FREE USAGE LIMITS

| Tool | Free Limit |
|---|---|
| gTTS (Tagalog TTS) | Unlimited |
| Whisper (Captions) | Unlimited |
| FFmpeg (Video) | Unlimited |
| YouTube API | 10,000 units/day (~5-6 uploads) |
| TikTok API | Varies by account age |
| Ollama (Story AI) | Unlimited (runs locally) |

---

*Built with 🍎 using Python — 100% free tools*
