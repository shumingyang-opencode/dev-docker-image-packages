---
name: ddip-image-create
description: Create a new Docker image in the dev-docker-image-packages project. Interactive workflow that asks about purpose, recommends tools, configures environment variables, and optionally adds Python scripts. Automatically generates Dockerfile, README.md, and updates index. Use when the user says "加 image", "new image", "create image", "新增 image", "scaffold image", "add image".
compatibility: needs git + gh (GitHub CLI)
---

# ddip-image-create

Create a new Docker image in `dev-docker-image-packages/images/<name>/`.

## Step 1: Requirements Discussion

Ask the user:

1. **Image name** — short kebab-case name, e.g. `python-ml`, `node`, `go`
   - Must match `^[a-z][a-z0-9-]*$`
   - Confirm it doesn't already exist in `images/`

2. **Base image** — what FROM to use?
   - Default recommendation: `ghcr.io/shumingyang-opencode/python:latest` (our own base)
   - Alternatives: `python:3.13-slim`, `ubuntu:24.04`, `node:22-slim`, `scratch`, etc.

3. **Purpose** — one sentence describing what this image is for
   - Used to generate README.md and to recommend tools

## Step 2: Recommend Components

Based on the purpose, suggest and let the user confirm each category:

### System Packages
```
☐ git           ☐ curl           ☐ build-essential
☐ ca-certificates ☐ tzdata       ☐ unzip
☐ jq            ☐ yq             ☐ ...
```

### Python Tools (if Python-based)
```
☐ poetry        ☐ ruff           ☐ mypy
☐ pytest        ☐ black          ☐ pre-commit
☐ pipx          ☐ ...
```

### AI CLI Tools (always suggest if dev-oriented)
```
☐ OpenCode CLI       (npm i -g opencode-ai)
☐ GitHub Copilot CLI (npm i -g @github/copilot)
☐ Google Gemini CLI  (npm i -g @google/gemini-cli)
☐ Lark CLI           (npm i -g @larksuite/cli)
☐ Trae CLI           (sh -c "$(curl -L https://trae.cn/trae-cli/install.sh)")
```

### Other Language Runtimes
```
☐ Node.js    ☐ Go    ☐ Rust    ☐ Java
```

## Step 3: Environment Variables

Ask and recommend:
```
☐ TZ=Asia/Taipei
☐ PYTHONUNBUFFERED=1
☐ POETRY_VERSION=<latest>
☐ Custom: __________
```

## Step 4: Python Scripts

"Would you like to include custom Python scripts in the image?"
```
☐ entrypoint.py     — runs on container start
☐ healthcheck.py    — health check endpoint
☐ custom script     — user provides content
```

If yes, create `images/<name>/scripts/` and put the scripts there, then add `COPY` lines to Dockerfile.

## Step 5: Generate Files

### `images/<name>/Dockerfile`

```
FROM <base>
LABEL org.opencontainers.image.version="0.1.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
    <selected-system-packages> \
    && rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Taipei
<other env vars>

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir <selected-python-tools>

RUN npm install -g <selected-npm-tools>
RUN sh -c "$(curl -L https://trae.cn/trae-cli/install.sh)"

<COPY scripts if any>

RUN useradd -m devuser
```

### `images/<name>/README.md`

Generate based on user's answers:
- 功能描述
- Base Image
- 版本
- 預裝工具清單（表格）
- 建議用途
- 使用方式（`docker pull ghcr.io/...`）

### Update `images/README.md`

Add a row to the index table.

### Update root `README.md`

Update the image table in the root README.

## Step 6: Final Confirmation

Show summary:
```
Image:      python-ml
Base:       ghcr.io/shumingyang-opencode/python:latest
Version:    0.1.0
System:     git, curl, build-essential
Python:     poetry, ruff, numpy, pandas
AI CLI:     opencode, copilot
Scripts:    entrypoint.py
```

Ask:
- "Commit this to git? (y/n)"
- If yes: `git add images/ && git commit -m "feat: add <name> image"`
