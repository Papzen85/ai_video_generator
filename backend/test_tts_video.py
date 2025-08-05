from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import pyttsx3
import uuid
import os

# Generate TTS audio
tts_engine = pyttsx3.init()
tts_text = "Hello world. This is a test of the AI video generator."
tts_audio_path = f"tts_{uuid.uuid4().hex}.wav"
tts_engine.save_to_file(tts_text, tts_audio_path)
tts_engine.runAndWait()

# Create an image frame with text
img = Image.new('RGB', (640, 360), color='black')
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("arial.ttf", 40)
except:
    font = ImageFont.load_default()
draw.text((20, 150), tts_text, font=font, fill='white')

img_path = f"frame_{uuid.uuid4().hex}.png"
img.save(img_path)

# Load image clip and audio clip
clip = ImageClip(img_path).set_duration(5)
audio = AudioFileClip(tts_audio_path)

# Add audio to video clip
video = clip.set_audio(audio)

# Output path
output_path = f"test_output_{uuid.uuid4().hex}.mp4"

# Write video file
video.write_videofile(output_path, fps=24)

print("Video generated:", output_path)
