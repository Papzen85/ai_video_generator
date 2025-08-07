FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavutil-dev \
    libswscale-dev \
    libasound2-dev \
    libpulse-dev \
    libffi-dev \
    libssl-dev \
    liblzma-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    wget \
    vim \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./backend /app/backend
COPY ./backend/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 10000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]
