"""
uploader.py
Uploads videos to YouTube (free API) and TikTok.

YouTube: Uses Google's free YouTube Data API v3
TikTok: Uses TikTok Content Posting API (free developer account)

Setup instructions are in README.md
"""

import os
import json
import pickle
from datetime import datetime, timedelta


# ── YOUTUBE UPLOAD ──────────────────────────────────────────────────────────

def upload_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: list,
    category_id: str = "22",       # 22 = People & Blogs
    privacy: str = "public"
) -> str:
    """
    Upload video to YouTube using YouTube Data API v3.
    Returns the YouTube video ID on success.

    Requirements:
        pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
    """
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request

        print(f"  📺 Uploading to YouTube...")

        youtube = get_youtube_service()

        request_body = {
            "snippet": {
                "title": title[:100],            # YouTube title limit: 100 chars
                "description": description[:5000],
                "tags": tags[:500],
                "categoryId": category_id,
                "defaultLanguage": "tl",          # Tagalog
                "defaultAudioLanguage": "tl",
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False,
            }
        }

        media = MediaFileUpload(
            video_path,
            mimetype="video/mp4",
            resumable=True,
            chunksize=1024 * 1024 * 5  # 5MB chunks
        )

        upload_request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = upload_request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"  📤 YouTube upload progress: {progress}%")

        video_id = response["id"]
        video_url = f"https://youtube.com/watch?v={video_id}"
        print(f"  ✅ YouTube upload complete!")
        print(f"  🔗 URL: {video_url}")
        return video_id

    except ImportError:
        print("  ❌ YouTube API libraries not installed.")
        print("  Run: pip install google-api-python-client google-auth-oauthlib")
        return None
    except Exception as e:
        print(f"  ❌ YouTube upload error: {e}")
        return None


def get_youtube_service():
    """
    Authenticate and return YouTube API service.
    First run opens a browser for Google login — saves token for future runs.
    """
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    TOKEN_FILE = "youtube_token.pickle"
    CREDENTIALS_FILE = "client_secrets.json"   # Download from Google Console

    creds = None

    # Load saved token
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    # Refresh or re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Missing {CREDENTIALS_FILE}! "
                    "Download it from Google Cloud Console → APIs → Credentials."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next time
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)


# ── TIKTOK UPLOAD ────────────────────────────────────────────────────────────

def schedule_tiktok(video_path: str, title: str) -> bool:
    """
    Post video to TikTok using the Content Posting API.

    Requirements:
        pip install requests
        Set TIKTOK_ACCESS_TOKEN in your .env file
    """
    print(f"  🎵 Posting to TikTok...")

    access_token = os.getenv("TIKTOK_ACCESS_TOKEN")

    if not access_token:
        print("  ⚠️  TIKTOK_ACCESS_TOKEN not set in .env")
        print("  ℹ️  See README.md for TikTok setup instructions")
        print("  💡 Alternative: Use TikTok's free native scheduler at tiktok.com/creator-center")
        return False

    try:
        import requests

        # Step 1: Initialize upload
        init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8"
        }

        file_size = os.path.getsize(video_path)

        init_payload = {
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": file_size,
                "total_chunk_count": 1
            }
        }

        init_response = requests.post(init_url, json=init_payload, headers=headers)
        init_data = init_response.json()

        if init_response.status_code != 200:
            print(f"  ❌ TikTok init error: {init_data}")
            return False

        upload_url = init_data["data"]["upload_url"]
        publish_id = init_data["data"]["publish_id"]

        # Step 2: Upload video file
        with open(video_path, "rb") as video_file:
            video_data = video_file.read()

        upload_headers = {
            "Content-Range": f"bytes 0-{file_size-1}/{file_size}",
            "Content-Type": "video/mp4"
        }

        upload_response = requests.put(upload_url, data=video_data, headers=upload_headers)

        if upload_response.status_code not in [200, 201]:
            print(f"  ❌ TikTok upload error: {upload_response.status_code}")
            return False

        print(f"  ✅ TikTok video uploaded! Publish ID: {publish_id}")
        print(f"  ℹ️  Video will appear in your TikTok drafts within 5 minutes.")
        return True

    except Exception as e:
        print(f"  ❌ TikTok error: {e}")
        return False
