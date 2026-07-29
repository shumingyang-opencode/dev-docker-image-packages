[繁體中文](./README.md) · [**English**](./README.en.md) · [简体中文](./README.zh-CN.md)

---

# Dev Docker Image Packages

![GitHub Release](https://img.shields.io/github/v/release/shumingyang-opencode/dev-docker-image-packages)
![GHCR Pulls](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fghcr.io%2Fv2%2Fshumingyang-opencode%2Fpy-devkit-image-base&label=GHCR%20pulls&query=%24.pull_count)
![GitHub Actions Workflow](https://img.shields.io/github/actions/workflow/status/shumingyang-opencode/dev-docker-image-packages/build-image.yml)

A collection of personal Docker images, automatically built and published to GHCR via GitHub Actions.

## Quick Start

```bash
# 1. Pull the latest image
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:latest

# 2. Start a dev container
docker run --rm -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 3. Check the built-in AI CLIs
opencode --version && copilot --help && lark-cli --version && trae-cli --version
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- GitHub account (to trigger CI builds and E2E tests)
- API keys for each AI CLI (required for Advanced E2E tests)

> To simply **pull and run** an image, you only need Docker — no GitHub account required.

## Available Images

| Image | Latest Version | Base | Description | Docs |
|-------|---------------|------|-------------|------|
| [py-devkit-image-base](./images/py-devkit-image-base/) | 1.4.0 | python:3.12-slim | Python dev environment (AI CLIs, trae-agent, trae-cli config) | [README](./images/py-devkit-image-base/README.md) |

> For a full image index, see [images/README.md](./images/README.md).

## Built-in AI CLI Tools

| CLI | Package | Description | Needs API Key |
|-----|---------|-------------|:-------------:|
| `opencode` | npm (opencode-ai) | AI development assistant | ✅ |
| `copilot` | npm (@github/copilot) | GitHub Copilot Agent | ✅ |
| `lark-cli` | npm (@larksuite/cli) | Lark development CLI (internal network only) | ❌ |
| `trae-cli` | pip (trae-agent) | AI Code Agent | ✅ |

> API keys are passed via environment variables. See each image's README for details.

## Image Tags

Each image is published to GHCR with the following tags:

| Tag | Description |
|-----|-------------|
| `latest` | Updated on every build |
| `{version}` | Also updated on every build — both tags point to the same content |

Use `latest` for the most up-to-date version. Version tags (e.g., `1.4.0`) are available but are updated simultaneously with each build.

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
| **E2E: Basic Agent** (Basic E2E) | [`test-e2e-basic.yml`](./.github/workflows/test-e2e-basic.yml) | Manual | Cross-image agent binary + version check |
| **E2E: Advanced Prompt** (Advanced E2E) | [`test-e2e-advanced.yml`](./.github/workflows/test-e2e-advanced.yml) | Manual | Custom prompt + model selection (free models) agent test (needs API keys) |

### Trigger via gh CLI

```bash
# Build + Smoke test
gh workflow run build-image.yml -f image=py-devkit-image-base
gh workflow run build-image.yml -f image=all

# Install check
gh workflow run test-image.yml -f image=py-devkit-image-base

# Engine load check
gh workflow run test-run-image.yml -f image=py-devkit-image-base

# E2E tests (Basic)
gh workflow run test-e2e-basic.yml -f image=py-devkit-image-base

# E2E tests (Advanced — use free model)
gh workflow run test-e2e-advanced.yml \
  -f image=py-devkit-image-base \
  -f agent=trae-cli \
  -f prompt="Say hello" \
  -f model="google/gemma-4-26b-a4b-it:free" \
  -f openrouter_api_key=sk-or-...
```

> The test scripts (`test-smoke.sh` / `test-run.sh`) can also be run locally. See each image's README for details.

## E2E Tests

The project provides two levels of E2E testing in [`tests/e2e/`](./tests/e2e/README.md):

| Test | Language | Needs API Key | Description |
|------|----------|--------------|-------------|
| **Basic E2E** | Python + pytest | No | Cross-image agent binary + `--version`/`--help` check |
| **Advanced E2E** | Python + pytest | Yes (per agent) | Custom prompt agent test with selectable LLM model |

### Basic E2E

Pulls the published image and verifies each agent binary exists and is executable. No authentication required.

```bash
gh workflow run test-e2e-basic.yml -f image=py-devkit-image-base
```

### Advanced E2E

Pulls the published image, runs a custom prompt through the selected agent using your API key, and validates the response.

```bash
gh workflow run test-e2e-advanced.yml \
  -f image=py-devkit-image-base \
  -f agent=trae-cli \
  -f prompt="Write a Python hello world" \
  -f model="google/gemma-4-26b-a4b-it:free" \
  -f openrouter_api_key=sk-or-...
```

Parameters:

| Parameter | Description |
|-----------|-------------|
| `image` | Image name (dropdown) |
| `tag` | Image tag (default `latest`) |
| `agent` | Agent to test (dropdown) |
| `prompt` | Custom prompt text |
| `model` | LLM model selector (dropdown, free OpenRouter models only) |
| `timeout` | Timeout in seconds (default 120) |
| `*_api_key` | Agent-specific API keys (manual input, not stored as secrets) |

### Run Locally

```bash
# Basic E2E
pytest tests/e2e/test_basic.py --image py-devkit-image-base --tag latest -v

# Advanced E2E
export OPENROUTER_API_KEY=sk-or-...
pytest tests/e2e/test_advanced.py \
  --image py-devkit-image-base \
  --agent trae-cli \
  --prompt "Say hello" \
  --model "google/gemma-4-26b-a4b-it:free" \
  -v --tb=short -s
```

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

## Contributing

PRs and feature requests are welcome:

1. **Add a new image** — Create `images/<name>/` with a Dockerfile + test scripts, then add the agent config in `tests/e2e/agents/`
2. **Improve tests** — Strengthen E2E test coverage or add new test cases
3. **Documentation** — Fix typos, clarify instructions, or improve docs quality

How to contribute: Fork → Develop → Submit a PR → I'll review and merge.

## Related Projects

- [OpenCode](https://opencode.ai) — AI development assistant (built into this image)
- [trae-agent](https://github.com/bytedance/trae-agent) — ByteDance open-source AI Agent
- [GHCR](https://ghcr.io) — GitHub Container Registry

## License

MIT

## Project Structure

```
├── docs/                    Development docs
│   └── trae-cli-auth.md          trae-cli authentication guide
├── .github/workflows/        GitHub Actions workflows
│   ├── build-image.yml           Build + Smoke test
│   ├── test-image.yml            Manual smoke test
│   ├── test-run-image.yml        Manual run test
│   ├── test-e2e-basic.yml        E2E Basic (no auth)
│   └── test-e2e-advanced.yml     E2E Advanced (needs API keys)
├── images/                   Docker image definitions
│   ├── README.md                 Image index
│   └── <name>/
│       ├── README.md             Image documentation
│       ├── Dockerfile            Build script
│       ├── test-smoke.sh         Smoke test (install verification)
│       └── test-run.sh           Run test (engine load verification)
├── tests/                    E2E Tests
│   └── e2e/
│       ├── conftest.py            Shared fixtures
│       ├── test_basic.py          Basic E2E (no auth)
│       ├── test_advanced.py       Advanced E2E (needs API keys)
│       ├── agents/                Per-image agent configs
│       └── README.md              E2E test documentation
├── skills/                   OpenCode Skills
│   └── install.sh            Installation script
| README.md                    Traditional Chinese (default)
├── README.en.md               English
├── README.zh-CN.md            Simplified Chinese
```
