# VidCraft — Local Deployment Guide (Minimal)

This archive contains a runnable minimal VidCraft project skeleton for local testing and Render deployment.
It includes:
- backend/ (FastAPI)
- frontend/ (React + Tailwind skeleton)
- Dockerfile (Python 3.11, FFmpeg installed)
- render.yaml (Render Docker service config)
- requirements.txt (. includes python-multipart and pydub)
- .gitignore

## Quick local run (recommended using Docker Compose)

1. Install Docker & Docker Compose.
2. From this folder, run:
   ```bash
   docker build -t vidcraft-backend .
   docker run --rm -p 10000:10000 vidcraft-backend
   ```
   Or use the provided `docker-compose.yml` if you add one.

## Without Docker (Windows)

1. Install Python 3.11.
2. Install ffmpeg (add to PATH).
3. Create venv:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn backend.main:app --host 0.0.0.0 --port 10000
   ```

## Notes & Troubleshooting
- If you see `ModuleNotFoundError: No module named 'pyaudioop'`:
  - On Debian-based images, install `libpython3-dev` and `build-essential` before `pip install`.
  - The provided Dockerfile already installs necessary system packages.
- `python-multipart` is required for form/file multipart parsing — it's in requirements.txt.
- MoviePy needs `ffmpeg` available; Dockerfile installs it.
- Stable Video Diffusion integration is a stub in `backend/svd_integration.py` — replace with your SVD endpoint / model as needed.
