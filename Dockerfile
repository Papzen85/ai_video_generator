# Use Python 3.11 to avoid pyaudioop issues with 3.13
FROM python:3.11-slim

# Install system deps for ffmpeg, building extensions and fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libsndfile1 \
    libasound2-dev \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libsdl2-dev \
    libpython3.11-dev \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 10000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]
