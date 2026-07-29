FROM python:3.12-slim
LABEL org.opencontainers.image.version="1.4.0"

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    build-essential \
    tzdata \
    sqlite3 \
    fonts-noto-cjk \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Taipei
WORKDIR /workspace

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    poetry \
    ruff \
    mypy \
    pytest \
    duckdb

RUN npm install -g \
    opencode-ai \
    @github/copilot \
    @larksuite/cli \
    && npm cache clean --force

RUN pip install --no-cache-dir docker pexpect \
    && pip install --no-cache-dir git+https://github.com/bytedance/trae-agent.git

COPY trae_config.yaml /etc/trae/trae_config.yaml
ENV TRAE_CONFIG_FILE=/etc/trae/trae_config.yaml

RUN useradd -m devuser
