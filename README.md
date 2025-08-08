# VidCraft - Realistic Video Generation Scaffold
This scaffold provides a starting point to upgrade VidCraft with realistic AI video generation (Veo 3-style).
It contains a FastAPI backend, Celery task stubs, and modular placeholders for integrating AnimateDiff, Stable Video Diffusion,
Genmo/Pika/Runway APIs, and talking-head tools like D-ID and SadTalker.

## Structure
- backend/
  - main.py -- FastAPI app with a generate endpoint
  - celery_worker.py -- Celery app
  - tasks/ -- Celery task stubs
  - modules/ -- Integration adapters (prompt_to_clip, image_to_motion, etc.)

## Next steps to make realistic:
1. Install GPU-enabled libs (torch, accelerate) and AnimateDiff/SVD.
2. Replace stubs in modules/ with real model calls (HuggingFace, Pika API, Runway).
3. Configure Redis and Celery workers for async jobs.
4. Add authentication & quota management for users.

## How to run (dev)
```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# Celery worker (in separate terminal)
celery -A tasks.generate_realistic_video worker --loglevel=info
```
