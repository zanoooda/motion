FROM python:3.11-slim AS base
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app

FROM base AS debug
RUN pip install --no-cache-dir debugpy
CMD ["python","-m","debugpy","--listen","0.0.0.0:5678","--wait-for-client","/app/main.py"]

FROM base AS release
CMD ["python","/app/main.py"]