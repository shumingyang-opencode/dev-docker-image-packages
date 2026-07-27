[繁體中文](./README.md) · [**English**](./README.en.md) · [简体中文](./README.zh-CN.md)

---

# Dev Docker Image Packages

A collection of personal Docker images, automatically built and published to GHCR via GitHub Actions.

## Available Images

| Image | Latest Version | Base | Description | Docs |
|-------|---------------|------|-------------|------|
| [py-devkit-image-base](./images/py-devkit-image-base/) | 1.2.0 | python:3.12-slim | Python dev environment (AI CLIs, trae-agent) | [README](./images/py-devkit-image-base/README.md) |

> For a full image index, see [images/README.md](./images/README.md).

## Image Tags

Each image is published to GHCR with the following tags:

| Tag | Description |
|-----|-------------|
| `latest` | Updated on every build |
| `{version}` | Also updated on every build — both tags point to the same content |

Use `latest` for the most up-to-date version. Version tags (e.g., `1.2.0`) are available but are updated simultaneously with each build.

## Usage

### Pull the Image

```bash
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:latest
```

### Run the Container

```bash
# Basic usage
docker run --rm -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# Run as devuser (non-root)
docker run --rm --user devuser -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# Mount local workspace
docker run --rm -it -v $(pwd):/workspace ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# Pass API keys for AI CLIs
docker run --rm -it \
  -e OPENCODE_API_KEY=your_key \
  -e GEMINI_API_KEY=your_key \
  -e COPILOT_GITHUB_TOKEN=your_token \
  -v $(pwd):/workspace \
  ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash
```

### Docker Compose Integration

```yaml
services:
  dev:
    image: ghcr.io/shumingyang-opencode/py-devkit-image-base:latest
    container_name: py-devkit
    volumes:
      - .:/workspace
    environment:
      - OPENCODE_API_KEY=${OPENCODE_API_KEY:-}
      - GEMINI_API_KEY=${GEMINI_API_KEY:-}
      - COPILOT_GITHUB_TOKEN=${COPILOT_GITHUB_TOKEN:-}
    working_dir: /workspace
    stdin_open: true
    tty: true
```

### Use as a Base Image

```dockerfile
FROM ghcr.io/shumingyang-opencode/py-devkit-image-base:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

> For a full list of pre-installed tools and authentication methods, see [images/py-devkit-image-base/README.md](./images/py-devkit-image-base/README.md).

## CI / GitHub Actions Workflows

| Workflow | File | Trigger | Description |
|----------|------|---------|-------------|
| 建置 · Smoke 測試 (Build + Smoke) | [`build-image.yml`](./.github/workflows/build-image.yml) | Manual + Auto | Build → run smoke tests |
| Smoke 測試：CLI 已安裝 (Install Check) | [`test-image.yml`](./.github/workflows/test-image.yml) | Manual | Verify binaries are installed |
| 啟動測試：CLI 可執行 (Engine Load) | [`test-run-image.yml`](./.github/workflows/test-run-image.yml) | Manual | Verify CLI engines load correctly |

### Trigger via gh CLI

```bash
# Build + Smoke test
gh workflow run build-image.yml -f image=py-devkit-image-base
gh workflow run build-image.yml -f image=all

# Install check
gh workflow run test-image.yml -f image=py-devkit-image-base

# Engine load check
gh workflow run test-run-image.yml -f image=py-devkit-image-base
```

> The test scripts (`test-smoke.sh` / `test-run.sh`) can also be run locally. See each image's README for details.

## Skills (OpenCode Integration)

This repository provides OpenCode Skills for managing images through conversation.

### Install Skills

```bash
git clone https://github.com/shumingyang-opencode/dev-docker-image-packages.git
cd dev-docker-image-packages
bash skills/install.sh
```

### Available Commands

| Say | Effect |
|-----|--------|
| "幫我安裝位在 `https://github.com/...` 的技能" | Install all ddip skills from repo |
| "有哪些 image" / "list images" | List all available images |
| "加 image" / "new image" / "create image" | Scaffold a new image (Dockerfile + README) |
| "build image" / "建置 image" | Trigger GitHub Actions build for an image |

## Project Structure

```
├── .github/workflows/        GitHub Actions workflows
│   ├── build-image.yml           Build + Smoke test
│   ├── test-image.yml            Manual smoke test
│   └── test-run-image.yml        Manual run test
├── images/                   Docker image definitions
│   ├── README.md                 Image index
│   └── <name>/
│       ├── README.md             Image documentation
│       ├── Dockerfile            Build script
│       ├── test-smoke.sh         Smoke test (install verification)
│       └── test-run.sh           Run test (engine load verification)
├── skills/                   OpenCode Skills
│   └── install.sh            Installation script
| README.md                    Traditional Chinese (default)
├── README.en.md               English
├── README.zh-CN.md            Simplified Chinese
```
