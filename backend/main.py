from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
from moviepy.editor import ImageClip
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Backend is running!"}

@app.post("/generate")
async def generate_video(
    script: str = Form(...),
    voices: list[UploadFile] = File(None),
    background_music: UploadFile = File(None),
    character_image: UploadFile = File(None),
):
    script_lines = [line.strip() for line in script.split('.') if line.strip()]
    clips = []

    char_img = None
    if character_image:
        char_img_path = f"static/character_{uuid.uuid4().hex}.png"
        with open(char_img_path, "wb") as f:
            f.write(await character_image.read())
        char_img = Image.open(char_img_path).convert("RGB").resize((1280, 720))

    for i, line in enumerate(script_lines):
        if char_img:
            img = char_img.copy()
        else:
            img = Image.new('RGB', (1280, 720), color='black')

        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 48)
        except IOError:
            font = ImageFont.load_default()
        draw.text((50, 620), line, font=font, fill='white')

        img_path = f"static/frame_{uuid.uuid4().hex}.png"
        img.save(img_path)

        if voices and i < len(voices):
            voice_file = voices[i]
            voice_path = f"static/voice_{uuid.uuid4().hex}.mp3"
            with open(voice_path, "wb") as f:
                f.write(await voice_file.read())
            voice_audio = AudioFileClip(voice_path)
        else:
            silent_path = f"static/silent_{uuid.uuid4().hex}.mp3"
            AudioSegment.silent(duration=2000).export(silent_path, format="mp3")
            voice_audio = AudioFileClip(silent_path)

        clip = ImageClip(img_path).set_duration(voice_audio.duration)
        clip = clip.set_audio(voice_audio)
        clips.append(clip)

    final_video = concatenate_videoclips(clips)

    if background_music:
        music_path = f"static/music_{uuid.uuid4().hex}.mp3"
        with open(music_path, "wb") as f:
            f.write(await background_music.read())
        music = AudioFileClip(music_path).volumex(0.2)
        final_audio = CompositeAudioClip([final_video.audio, music])
        final_video = final_video.set_audio(final_audio)

    output_filename = f"output_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join("static", output_filename)

    final_video.write_videofile(output_path, fps=24)

    return {"video_url": f"/static/{output_filename}"}
