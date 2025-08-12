FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . .
EXPOSE 10000
CMD ["uvicorn","backend.main:app","--host","0.0.0.0","--port","10000"]
