from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uuid, os
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel

# import moviepy via local editor shim
from backend.editor import (
    VideoFileClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, AudioFileClip, CompositeAudioClip, ImageClip
)

# pydub used for silent audio creation
try:
    from pydub import AudioSegment
except Exception:
    AudioSegment = None

# Your local imports for enqueueing jobs
from modules import prompt_to_clip, image_to_motion, talking_avatar, style_transfer
from tasks.generate_realistic_video import enqueue_realistic_job

app = FastAPI(title="VidCraft Backend - Realistic Video Scaffold")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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
    # ensure multipart support
    try:
        import multipart  # type: ignore
    except Exception:
        raise HTTPException(status_code=500, detail='python-multipart is required. Add it to requirements.')

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

        # audio handling
        if voices and i < len(voices):
            voice_file = voices[i]
            voice_path = f"static/voice_{uuid.uuid4().hex}.mp3"
            with open(voice_path, "wb") as f:
                f.write(await voice_file.read())
            voice_audio = AudioFileClip(voice_path)
        else:
            silent_path = f"static/silent_{uuid.uuid4().hex}.mp3"
            if AudioSegment is None:
                # fallback: create a tiny silent file using moviepy
                from moviepy.audio.AudioClip import AudioArrayClip
                import numpy as np
                arr = np.zeros((44100*1,1))
                AudioArrayClip(arr, fps=44100).write_audiofile(silent_path)
            else:
                AudioSegment.silent(duration=2000).export(silent_path, format="mp3")
            voice_audio = AudioFileClip(silent_path)

        # create image clip with voice audio here (example, actual code may differ)
        clip = ImageClip(img_path).set_duration(2).set_audio(voice_audio)
        clips.append(clip)

    final_video = concatenate_videoclips(clips)
    output_path = f"static/output_{uuid.uuid4().hex}.mp4"
    final_video.write_videofile(output_path, fps=24)

    return {"status": "done", "video_path": output_path}

class PromptRequest(BaseModel):
    script: str
    mode: str = "realistic"  # realistic | animate | talking
    options: dict = {}

@app.post("/generate_realistic_clip")
async def generate_clip(req: PromptRequest, background_tasks: BackgroundTasks):
    """Endpoint that accepts a script chunk and queues a realistic clip job."""
    job_id = enqueue_realistic_job(req.script, req.mode, req.options)
    return {"status": "queued", "job_id": job_id}

@app.get("/health")
async def health():
    return {"status": "ok"}
