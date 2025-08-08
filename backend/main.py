from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from modules import prompt_to_clip, image_to_motion, talking_avatar, style_transfer
from tasks.generate_realistic_video import enqueue_realistic_job

app = FastAPI(title="VidCraft Backend - Realistic Video Scaffold")

class PromptRequest(BaseModel):
    script: str
    mode: str = "realistic"  # realistic | animate | talking
    options: dict = {}

@app.post("/generate_realistic_clip")
async def generate_clip(req: PromptRequest, background_tasks: BackgroundTasks):
    """Endpoint that accepts a script chunk and queues a realistic clip job."""
    # Enqueue a heavy job
    job_id = enqueue_realistic_job(req.script, req.mode, req.options)
    return {"status":"queued", "job_id": job_id}

@app.get("/health")
async def health():
    return {"status":"ok"}
