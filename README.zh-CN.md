[繁體中文](./README.md) · [English](./README.en.md) · [**简体中文**](./README.zh-CN.md)

---

# Dev Docker Image Packages

个人开发用 Docker Image 集合，通过 GitHub Actions 自动构建并发布至 GHCR。

## 可用 Images

| Image | 最新版本 | Base | 用途 | 说明文档 |
|-------|---------|------|------|---------|
| [py-devkit-image-base](./images/py-devkit-image-base/) | 1.4.0 | python:3.12-slim | Python 开发环境（含 AI CLI、trae-agent、trae-cli 配置文件） | [README](./images/py-devkit-image-base/README.md) |

> 详细 Image 索引请见 [images/README.md](./images/README.md)。

## Image Tags

每个 Image 发布至 GHCR 时会标记以下 tags：

| Tag | 说明 |
|-----|------|
| `latest` | 每次 build 更新至此 tag |
| `{version}` | 同一次 build 也会更新至此 tag，两者指向相同内容 |

建议使用 `latest` tag 获取最新版本。版本 tag（如 `1.4.0`）亦可使用，但每次重新构建时两者会同步更新。

## 使用方式

### 下载 Image

```bash
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:latest
```

### 运行容器

```bash
# 基本运行
docker run --rm -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 以 devuser 身份运行（非 root）
docker run --rm --user devuser -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 挂载本地工作目录
docker run --rm -it -v $(pwd):/workspace ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 传递 AI CLI 所需的 credentials
docker run --rm -it \
  -e OPENCODE_API_KEY=your_key \
  -e COPILOT_GITHUB_TOKEN=your_token \
  -v $(pwd):/workspace \
  ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash
```

### Docker Compose 整合

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

### 作为 Base Image

```dockerfile
FROM ghcr.io/shumingyang-opencode/py-devkit-image-base:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

> 各 Image 的预装工具清单与认证方式请见 [images/py-devkit-image-base/README.md](./images/py-devkit-image-base/README.md)。

## CI / GitHub Actions Workflows

| Workflow | 文件 | 触发方式 | 说明 |
|----------|------|---------|------|
| 建置 · Smoke 测试 (Build + Smoke) | [`build-image.yml`](./.github/workflows/build-image.yml) | 手动 + 自动（每次 build） | 构建 Image → 自动运行 Smoke test |
| Smoke 测试：CLI 已安装 (Install Check) | [`test-image.yml`](./.github/workflows/test-image.yml) | 手动按钮 | 验证指定版本的 binary 存在、可运行 |
| 启动测试：CLI 可运行 (Engine Load) | [`test-run-image.yml`](./.github/workflows/test-run-image.yml) | 手动按钮 | 验证指定版本的 CLI 引擎能加载 |
| **E2E 测试：基本 Agent** (Basic E2E) | [`test-e2e-basic.yml`](./.github/workflows/test-e2e-basic.yml) | 手动按钮 | 跨 Image 统一验证 Agent binary + version |
| **E2E 测试：进阶 Prompt** (Advanced E2E) | [`test-e2e-advanced.yml`](./.github/workflows/test-e2e-advanced.yml) | 手动按钮 | 自定义 Prompt + 选 Model（免费模型）测试 Agent 真实回应（需 API Key） |

### 手动触发 (gh CLI)

```bash
# 构建 + 自动测试
gh workflow run build-image.yml -f image=py-devkit-image-base
gh workflow run build-image.yml -f image=all

# 安装测试
gh workflow run test-image.yml -f image=py-devkit-image-base

# 引擎测试
gh workflow run test-run-image.yml -f image=py-devkit-image-base

# E2E 测试（Basic）
gh workflow run test-e2e-basic.yml -f image=py-devkit-image-base

# E2E 测试（Advanced — 使用免费模型）
gh workflow run test-e2e-advanced.yml \
  -f image=py-devkit-image-base \
  -f agent=trae-cli \
  -f prompt="Say hello" \
  -f model="google/gemma-4-26b-a4b-it:free" \
  -f openrouter_api_key=sk-or-...
```

> 各 Image 的测试脚本（`test-smoke.sh` / `test-run.sh`）可独立于 CI 在本地运行，详见各 Image 目录下的 README。

## E2E 测试

项目提供两层 E2E 测试，位于 [`tests/e2e/`](./tests/e2e/README.md)：

| 测试 | 语言 | 需 API Key | 说明 |
|------|------|-----------|------|
| **Basic E2E** | Python + pytest | 否 | 跨 Image 统一验证 Agent binary + `--version`/`--help` |
| **Advanced E2E** | Python + pytest | 是（视 Agent） | 自定义 Prompt 测试 Agent 真实回应，可选 LLM Model |

### Basic E2E

拉取已发布的 Image，逐一验证每个 Agent 的 binary 存在且可执行。无需任何认证。

```bash
gh workflow run test-e2e-basic.yml -f image=py-devkit-image-base
```

### Advanced E2E

拉取已发布的 Image，使用你提供的 API Key 对指定的 Agent 发送自定义 Prompt，验证回应。

```bash
gh workflow run test-e2e-advanced.yml \
  -f image=py-devkit-image-base \
  -f agent=trae-cli \
  -f prompt="Write a Python hello world" \
  -f model="google/gemma-4-26b-a4b-it:free" \
  -f openrouter_api_key=sk-or-...
```

支持参数：

| 参数 | 说明 |
|------|------|
| `image` | Image 名称（下拉菜单） |
| `tag` | Image tag（默认 `latest`） |
| `agent` | 要测试的 Agent（下拉菜单） |
| `prompt` | 自定义提示词 |
| `model` | LLM Model 选择（下拉，仅列出 OpenRouter 免费模型） |
| `timeout` | 超时秒数（默认 120） |
| `*_api_key` | 各 Agent 对应的 API Key（手动输入，不存于 Secrets） |

### 本地执行

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

## Skills（OpenCode 整合）

此项目提供 OpenCode Skills，让你可以通过对话操作 Image 生命周期。

### 安装 Skills

```bash
git clone https://github.com/shumingyang-opencode/dev-docker-image-packages.git
cd dev-docker-image-packages
bash skills/install.sh
```

### 可用指令

| 说 | 效果 |
|----|------|
| 「帮我安装位于 `https://github.com/...` 的技能」 | 从 repo 安装所有 ddip 技能 |
| 「有哪些 image」 / 「list images」 | 列出所有可用 Image |
| 「加 image」 / 「new image」 / 「create image」 | 互动式新增 Image（Dockerfile + README） |
| 「build image」 / 「建置 image」 | 触发 GitHub Actions 构建指定 Image |

## 项目目录结构

```
├── docs/                    开发文档
│   └── trae-cli-auth.md           trae-cli 认证说明
├── .github/workflows/        GitHub Actions workflows
│   ├── build-image.yml           构建 + Smoke 测试
│   ├── test-image.yml            手动 Smoke 测试
│   ├── test-run-image.yml        手动 Run 测试
│   ├── test-e2e-basic.yml        E2E Basic（无需认证）
│   └── test-e2e-advanced.yml     E2E Advanced（需 API Key）
├── images/                   Docker Image 定义
│   ├── README.md                 索引（所有 Image 列表）
│   └── <name>/
│       ├── README.md             该 Image 的详细说明
│       ├── Dockerfile            构建脚本
│       ├── test-smoke.sh         Smoke test（安装验证）
│       └── test-run.sh           Run test（引擎加载验证）
├── tests/                    E2E 测试
│   └── e2e/
│       ├── conftest.py            共用 fixtures
│       ├── test_basic.py          Basic E2E（无需认证）
│       ├── test_advanced.py       Advanced E2E（需 API Key）
│       ├── agents/                各 Image 的 Agent 配置文件
│       └── README.md              E2E 测试说明
├── skills/                   OpenCode Skills
│   └── install.sh            安装脚本
├── README.md                     繁體中文（預設）
├── README.en.md                   English
├── README.zh-CN.md                简体中文
```
