# Use Python 3.11 to avoid pyaudioop error with 3.13
FROM python:3.11-slim

# Install ffmpeg for pydub
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy everything into container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the backend on port 10000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]
