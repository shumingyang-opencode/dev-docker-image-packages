[繁體中文](./README.md) · [English](./README.en.md) · [**简体中文**](./README.zh-CN.md)

---

# Dev Docker Image Packages

个人开发用 Docker Image 集合，通过 GitHub Actions 自动构建并发布至 GHCR。

## 可用 Images

| Image | 最新版本 | Base | 用途 | 说明文档 |
|-------|---------|------|------|---------|
| [py-devkit-image-base](./images/py-devkit-image-base/) | 1.2.0 | python:3.12-slim | Python 开发环境（含 AI CLI、trae-agent） | [README](./images/py-devkit-image-base/README.md) |

> 详细 Image 索引请见 [images/README.md](./images/README.md)。

## Image Tags

每个 Image 发布至 GHCR 时会标记以下 tags：

| Tag | 说明 |
|-----|------|
| `latest` | 每次 build 更新至此 tag |
| `{version}` | 同一次 build 也会更新至此 tag，两者指向相同内容 |

建议使用 `latest` tag 获取最新版本。版本 tag（如 `1.2.0`）亦可使用，但每次重新构建时两者会同步更新。

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
  -e GEMINI_API_KEY=your_key \
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
      - GEMINI_API_KEY=${GEMINI_API_KEY:-}
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
| **E2E 测试：进阶 Prompt** (Advanced E2E) | [`test-e2e-advanced.yml`](./.github/workflows/test-e2e-advanced.yml) | 手动按钮 | 自定义 Prompt 测试 Agent 真实回应（需 API Key） |

### 手动触发 (gh CLI)

```bash
# 构建 + 自动测试
gh workflow run build-image.yml -f image=py-devkit-image-base
gh workflow run build-image.yml -f image=all

# 安装测试
gh workflow run test-image.yml -f image=py-devkit-image-base

# 引擎测试
gh workflow run test-run-image.yml -f image=py-devkit-image-base

# E2E 测试
gh workflow run test-e2e-basic.yml -f image=py-devkit-image-base
gh workflow run test-e2e-advanced.yml -f image=py-devkit-image-base -f agent=opencode -f prompt="Say hello"
```

> 各 Image 的测试脚本（`test-smoke.sh` / `test-run.sh`）可独立于 CI 在本地运行，详见各 Image 目录下的 README。

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
├── .github/workflows/        GitHub Actions workflows
│   ├── build-image.yml           构建 + Smoke 测试
│   ├── test-image.yml            手动 Smoke 测试
│   └── test-run-image.yml        手动 Run 测试
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
│       └── agents/                各 Image 的 Agent 配置文件
├── skills/                   OpenCode Skills
│   └── install.sh            安装脚本
├── README.md                     繁體中文（預設）
├── README.en.md                   English
├── README.zh-CN.md                简体中文
```
