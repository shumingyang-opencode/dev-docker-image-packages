FROM python:3.13-slim
LABEL org.opencontainers.image.version="1.0.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    build-essential \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Taipei

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    poetry \
    ruff \
    mypy \
    pytest

RUN useradd -m devuser
