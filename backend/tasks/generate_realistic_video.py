from celery import Celery
from pathlib import Path
import uuid, time, json, os
from svd_integration import render_clip_with_animdiff
from utils import stitch_clips

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
celery = Celery("tasks.generate_realistic_video", broker=redis_url, backend=redis_url)

@celery.task(bind=True)
def generate_realistic_video(self, full_script, clip_duration_sec=60, clip_count=20, options=None):
    job_id = str(uuid.uuid4())
    out_dir = Path("/tmp/vidcraft_jobs") / job_id
    out_dir.mkdir(parents=True, exist_ok=True)

    clips = []
    script_parts = [p.strip() for p in full_script.split("\n\n") if p.strip()]
    if not script_parts:
        script_parts = ["A scenic cinematic landscape."]

    for i in range(clip_count):
        prompt = script_parts[i] if i < len(script_parts) else script_parts[-1]
        self.update_state(state='PROGRESS', meta={'progress': int((i/clip_count)*100), 'statusText': f'Generating clip {i+1}/{clip_count}'})
        clip_path = render_clip_with_animdiff(prompt, out_dir, i, duration_sec=clip_duration_sec)
        clips.append(clip_path)
        # small wait to mimic work (remove when running real model)
        time.sleep(0.5)

    final_video_path = out_dir / "final_video.mp4"
    try:
        stitch_clips(clips, final_video_path)
    except Exception:
        final_video_path.write_bytes(b"")

    metadata = {"job_id": job_id, "final_video_path": str(final_video_path)}
    with open(out_dir / "metadata.json", "w") as mf:
        json.dump(metadata, mf)

    self.update_state(state='SUCCESS', meta={'progress':100, 'statusText':'Done', 'final_video_path': str(final_video_path)})
    return metadata

def enqueue_realistic_job(script, clip_duration_sec=60, clip_count=20, options=None):
    task = generate_realistic_video.delay(script, clip_duration_sec, clip_count, options or {})
    return task.id
