"""
tts_generator.py
Converts Tagalog story text to speech using gTTS (Google Text-to-Speech).
100% FREE — no API key needed. Uses Google's free TTS service.

Install: pip install gtts
"""

from gtts import gTTS
import os


def generate_tagalog_audio(text: str, output_path: str) -> str:
    """
    Convert Tagalog text to MP3 audio using gTTS.

    Args:
        text: The Tagalog story text
        output_path: Where to save the MP3 file

    Returns:
        Path to the generated audio file
    """
    print(f"  🎙️  Converting text to Tagalog speech...")
    print(f"  📄 Text length: {len(text)} characters")

    try:
        # 'tl' is the language code for Tagalog/Filipino
        tts = gTTS(text=text, lang='tl', slow=False)
        tts.save(output_path)

        # Check file was created
        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"  ✅ Audio saved ({size_kb:.1f} KB): {output_path}")
            return output_path
        else:
            raise Exception("Audio file was not created")

    except Exception as e:
        print(f"  ❌ gTTS error: {e}")
        print("  ℹ️  Make sure you have internet connection for gTTS.")
        raise


def split_text_for_tts(text: str, max_chars: int = 500) -> list:
    """
    Split long text into chunks for TTS processing.
    gTTS works best with shorter segments.

    Args:
        text: Full story text
        max_chars: Maximum characters per chunk

    Returns:
        List of text chunks
    """
    sentences = text.replace("。", ".").split(".")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def generate_audio_with_pause(text: str, output_path: str) -> str:
    """
    Generate audio with natural pauses between sentences.
    Uses pydub to merge multiple audio chunks with silence.

    Install: pip install pydub gtts
    """
    try:
        from pydub import AudioSegment
        import tempfile

        chunks = split_text_for_tts(text)
        audio_segments = []

        print(f"  🎙️  Generating audio in {len(chunks)} chunk(s)...")

        for i, chunk in enumerate(chunks):
            temp_file = f"temp_chunk_{i}.mp3"
            tts = gTTS(text=chunk, lang='tl', slow=False)
            tts.save(temp_file)

            segment = AudioSegment.from_mp3(temp_file)
            audio_segments.append(segment)

            # Add 0.5 second pause between sentences
            pause = AudioSegment.silent(duration=500)
            audio_segments.append(pause)

            os.remove(temp_file)

        # Merge all segments
        final_audio = audio_segments[0]
        for seg in audio_segments[1:]:
            final_audio = final_audio + seg

        final_audio.export(output_path, format="mp3")
        print(f"  ✅ Audio with pauses saved: {output_path}")
        return output_path

    except ImportError:
        # Fallback to simple gTTS without pauses
        print("  ℹ️  pydub not installed, using simple TTS...")
        return generate_tagalog_audio(text, output_path)
