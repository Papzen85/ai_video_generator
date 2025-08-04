from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import os

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure 'static' directory exists for output videos
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Input model
class ScriptInput(BaseModel):
    script: str

# Route for video generation
@app.post("/generate")
async def generate_video(data: ScriptInput):
    from moviepy.editor import TextClip, concatenate_videoclips  # Moved import inside route

    # Use only the first 3 lines/sentences
    script_lines = data.script.split('.')[:3]
    clips = []

    for line in script_lines:
        text = line.strip()
        if text:
            txt_clip = TextClip(text, fontsize=48, color='white', size=(640, 360))
            txt_clip = txt_clip.set_duration(10)
            clips.append(txt_clip)

    final_video = concatenate_videoclips(clips)
    filename = f"output_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join("static", filename)

    final_video.write_videofile(output_path, fps=24)

    return {"video_url": f"/static/{filename}"}
