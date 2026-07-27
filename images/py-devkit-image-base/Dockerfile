FROM python:3.13-slim
LABEL org.opencontainers.image.version="1.1.2"

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
    @google/gemini-cli \
    @larksuite/cli \
    && npm cache clean --force

# Trae Agent (open-source, https://github.com/bytedance/trae-agent)
# 目前已暫停安裝 — tree-sitter-languages 尚未支援 Python 3.13
# 待上游釋出 cp313 wheel 後即可取消註解：
# RUN pip install --no-cache-dir git+https://github.com/bytedance/trae-agent.git

RUN useradd -m devuser
