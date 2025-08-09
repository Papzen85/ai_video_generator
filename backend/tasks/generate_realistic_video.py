@celery.task(bind=True)
def generate_realistic_clip(self, script, mode='realistic', options=None):
    job_id = str(uuid.uuid4())
    out_dir = Path("/tmp/vidcraft_jobs") / job_id
    out_dir.mkdir(parents=True, exist_ok=True)

    total_clips = 20
    clip_length_seconds = 60  # conceptual length

    clips_metadata = []

    for clip_num in range(total_clips):
        self.update_state(state='PROGRESS', meta={'step': clip_num + 1, 'total': total_clips})
        # Simulate time taken per clip (adjust as needed)
        time.sleep(1)

        # Create placeholder file per clip
        video_path = out_dir / f"clip_{clip_num + 1}_preview.mp4"
        with open(video_path, "wb") as f:
            f.write(b"")  # placeholder empty file; replace with real video bytes

        # Store metadata per clip
        clips_metadata.append({
            "clip_number": clip_num + 1,
            "length_seconds": clip_length_seconds,
            "path": str(video_path)
        })

    metadata = {
        "job_id": job_id,
        "script": script,
        "mode": mode,
        "clips": clips_metadata,
    }

    with open(out_dir / "metadata.json", "w") as mf:
        json.dump(metadata, mf)

    return metadata
