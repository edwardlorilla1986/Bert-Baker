import whisper
import moviepy.editor as mp
import ffmpeg
import os
from elevenlabs import set_api_key, generate, save

# Step 1: Set ElevenLabs API Key from GitHub Secrets
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
set_api_key(ELEVENLABS_API_KEY)

# Step 2: Define AI Voiceover Script
script_text = "Welcome to our YouTube Shorts! Let's explore the amazing world of AI."

# Step 3: Generate AI Speech from Text
audio = generate(text=script_text, voice="Rachel")  # Change voice if needed
audio_filename = "ai_voiceover.mp3"
save(audio, audio_filename)

# Step 4: Transcribe AI Voiceover to Text (Whisper)
model = whisper.load_model("small")  # Use "medium" or "large" for better accuracy
transcription = model.transcribe(audio_filename)

# Step 5: Create FFmpeg Subtitle Filter File
subtitle_filename = "subtitles_filter.txt"

with open(subtitle_filename, "w") as f:
    for segment in transcription["segments"]:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"].replace("'", "’")  # Fix single quote issue
        f.write(
            f"drawtext=text='{text}':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,{start_time},{end_time})'\n"
        )

# Step 6: Load Video & Sync AI Voiceover
video_filename = "background_video.mp4"  # Ensure this file exists in the repo
video = mp.VideoFileClip(video_filename)
audio_clip = mp.AudioFileClip(audio_filename)
final_video = vi
