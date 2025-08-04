
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from moviepy.editor import TextClip, concatenate_videoclips
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

class ScriptInput(BaseModel):
    script: str

@app.post("/generate")
async def generate_video(data: ScriptInput):
    script = data.script.split('.')[:3]  # limit to 3 lines max
    clips = []
    for i, line in enumerate(script):
        txt_clip = TextClip(line.strip(), fontsize=48, color='white', size=(640, 360))
        txt_clip = txt_clip.set_duration(10)
        clips.append(txt_clip)

    final = concatenate_videoclips(clips)
    output_path = f"output_{uuid.uuid4().hex}.mp4"
    final.write_videofile(output_path, fps=24)

    return {"video_url": f"/static/{output_path}"}
