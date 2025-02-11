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

# Step 5: Convert Transcription into FFmpeg DrawText Format
subtitle_text = ""
for segment in transcription["segments"]:
    start_time = segment["start"]
    end_time = segment["end"]
    text = segment["text"]
    subtitle_text += f"drawtext=text='{text}':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,{start_time},{end_time})', "

subtitle_text = subtitle_text.rstrip(", ")

# Step 6: Load Video & Sync AI Voiceover
video_filename = "background_video.mp4"  # Ensure this file exists in the repo
video = mp.VideoFileClip(video_filename)
audio_clip = mp.AudioFileClip(audio_filename)
final_video = video.set_audio(audio_clip)
temp_video_no_subs = "temp_video.mp4"
final_video.write_videofile(temp_video_no_subs, codec="libx264", fps=30)

# Step 7: Burn Big Centered Subtitles Using FFmpeg
output_video_with_subs = "youtube_short_with_big_subtitles.mp4"

ffmpeg.input(temp_video_no_subs).output(
    output_video_with_subs,
    vf=subtitle_text,
    codec="libx264"
).run()

print("✅ YouTube Shorts video with BIG CENTERED subtitles created successfully!")
