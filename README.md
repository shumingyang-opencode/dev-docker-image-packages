[**繁體中文**](./README.md) · [English](./README.en.md) · [简体中文](./README.zh-CN.md)

---

# Dev Docker Image Packages

![GitHub Actions Workflow](https://img.shields.io/github/actions/workflow/status/shumingyang-opencode/dev-docker-image-packages/build-image.yml)
![Last Commit](https://img.shields.io/github/last-commit/shumingyang-opencode/dev-docker-image-packages)
![License](https://img.shields.io/badge/license-MIT-blue)

個人開發用 Docker Image 集合，透過 GitHub Actions 自動建置並發佈至 GHCR。

## 目錄

- [Quick Start](#quick-start)
- [需求](#需求)
- [可用 Images](#可用-images)
- [內建 AI CLI 工具](#內建-ai-cli-工具)
- [Image Tags](#image-tags)
- [使用方式](#使用方式)
- [CI / GitHub Actions Workflows](#ci--github-actions-workflows)
- [E2E 測試](#e2e-測試)
- [Skills（OpenCode 整合）](#skillsopencode-整合)
- [貢獻](#貢獻)
- [相關專案](#相關專案)
- [License](#license)
- [專案目錄結構](#專案目錄結構)

---

## Quick Start

```bash
# 1. 下載最新 Image
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:latest

# 2. 啟動開發容器
docker run --rm -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 3. 查看內建 AI CLI
opencode --version && copilot --help && lark-cli --version && trae-cli --version
```

## 需求

- [Docker](https://docs.docker.com/get-docker/) 已安裝
- GitHub 帳號（用於觸發 CI 建置、E2E 測試）
- 各 AI CLI 對應的 API Key（Advanced E2E 測試用）

> 若只需要 **Pull & Run** Image，則只需要 Docker，不需要 GitHub 帳號。

## 可用 Images

| Image | 最新版本 | Base | 用途 | 說明文件 |
|-------|---------|------|------|---------|
| [py-devkit-image-base](./images/py-devkit-image-base/) | 1.4.0 | python:3.12-slim | Python 開發基底（含 AI CLI、trae-agent、trae-cli 設定檔） | [README](./images/py-devkit-image-base/README.md) |

> 詳細 Image 索引請見 [images/README.md](./images/README.md)。

## 內建 AI CLI 工具

| CLI | 安裝方式 | 用途 | 需 API Key |
|-----|---------|------|:----------:|
| `opencode` | npm (opencode-ai) | AI 開發助手 | ✅ |
| `copilot` | npm (@github/copilot) | GitHub Copilot Agent | ✅ |
| `lark-cli` | npm (@larksuite/cli) | 飛書開發工具（內部網路專用） | ❌ |
| `trae-cli` | pip (trae-agent) | AI Code Agent | ✅ |

> API Key 透過環境變數傳遞，詳見各 Image 說明文件。

## Image Tags

每個 Image 發佈至 GHCR 時會標記以下 tags：

| Tag | 說明 |
|-----|------|
| `latest` | 每次 build 更新至此 tag |
| `{version}` | 同一次 build 也會更新至此 tag，兩者指向相同內容 |

建議使用 `latest` tag 取得最新版本。若需鎖定特定版本的內容，可直接使用版本 tag（如 `1.4.0`），不過每次重新建置時兩者都會同步更新。

## 使用方式

### 下載 Image

```bash
# 最新版
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:latest

# 指定版本
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:1.4.0
```

### 執行容器

```bash
# 基本執行
docker run --rm -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 以 devuser 身份執行（非 root）
docker run --rm --user devuser -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 掛載本機工作目錄
docker run --rm -it -v $(pwd):/workspace ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 傳遞 AI CLI 所需的 credentials
docker run --rm -it \
  -e OPENCODE_API_KEY=your_key \
  -e COPILOT_GITHUB_TOKEN=your_token \
  -v $(pwd):/workspace \
  ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash
```

### 整合 Docker Compose

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

### 作為 Base Image

```dockerfile
FROM ghcr.io/shumingyang-opencode/py-devkit-image-base:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

> 各 Image 的預裝工具清單與認證方式請見 [images/py-devkit-image-base/README.md](./images/py-devkit-image-base/README.md)。

## CI / GitHub Actions Workflows

| Workflow | 檔案 | 觸發方式 | 說明 |
|----------|------|---------|------|
| 建置 · Smoke 測試 (Build + Smoke) | [`build-image.yml`](./.github/workflows/build-image.yml) | 手動 + 自動（每次 build） | 建置 Image → 自動跑 Smoke test |
| Smoke 測試：CLI 已安裝 (Install Check) | [`test-image.yml`](./.github/workflows/test-image.yml) | 手動按鈕 | 驗證指定版本的 binary 存在、可執行 |
| 啟動測試：CLI 可執行 (Engine Load) | [`test-run-image.yml`](./.github/workflows/test-run-image.yml) | 手動按鈕 | 驗證指定版本的 CLI 引擎能載入 |
| **E2E 測試：基本 Agent** (Basic E2E) | [`test-e2e-basic.yml`](./.github/workflows/test-e2e-basic.yml) | 手動按鈕 | 跨 Image 統一驗證 Agent binary + version |
| **E2E 測試：進階 Prompt** (Advanced E2E) | [`test-e2e-advanced.yml`](./.github/workflows/test-e2e-advanced.yml) | 手動按鈕 | 自訂 Prompt + 選 Model（免費模型）測試 Agent 真實回應（需 API Key） |

### 手動觸發 (gh CLI)

```bash
# 建置 + 自動測試
gh workflow run build-image.yml -f image=py-devkit-image-base
gh workflow run build-image.yml -f image=all

# Smoke 測試（驗證安裝）
gh workflow run test-image.yml -f image=py-devkit-image-base

# Run 測試（驗證引擎）
gh workflow run test-run-image.yml -f image=py-devkit-image-base

# E2E 測試（Basic）
gh workflow run test-e2e-basic.yml -f image=py-devkit-image-base

# E2E 測試（Advanced — 使用免費模型）
gh workflow run test-e2e-advanced.yml \
  -f image=py-devkit-image-base \
  -f agent=trae-cli \
  -f prompt="Say hello" \
  -f model="google/gemma-4-26b-a4b-it:free" \
  -f openrouter_api_key=sk-or-...
```

> 各 Image 的測試腳本（`test-smoke.sh` / `test-run.sh`）可獨立於 CI 在本機執行，詳見各 Image 目錄下的 README。

## E2E 測試

專案提供兩層 E2E 測試，位於 [`tests/e2e/`](./tests/e2e/README.md)：

| 測試 | 語言 | 需 API Key | 說明 |
|------|------|-----------|------|
| **Basic E2E** | Python + pytest | 否 | 跨 Image 統一驗證 Agent binary + `--version`/`--help` |
| **Advanced E2E** | Python + pytest | 是（視 Agent） | 自訂 Prompt 測試 Agent 真實回應，可選 LLM Model |

### Basic E2E

拉取已發佈的 Image，逐一驗證每個 Agent 的 binary 存在且可執行。無需任何認證。

```bash
gh workflow run test-e2e-basic.yml -f image=py-devkit-image-base
```

### Advanced E2E

拉取已發佈的 Image，使用你提供的 API Key 對指定的 Agent 發送自訂 Prompt，驗證回應。

```bash
gh workflow run test-e2e-advanced.yml \
  -f image=py-devkit-image-base \
  -f agent=trae-cli \
  -f prompt="Write a Python hello world" \
  -f model="google/gemma-4-26b-a4b-it:free" \
  -f openrouter_api_key=sk-or-...
```

支援參數：

| 參數 | 說明 |
|------|------|
| `image` | Image 名稱（下拉選單） |
| `tag` | Image tag（預設 `latest`） |
| `agent` | 要測試的 Agent（下拉選單） |
| `prompt` | 自訂提示詞 |
| `model` | LLM Model 選擇（下拉，僅列出 OpenRouter 免費模型） |
| `timeout` | 超時秒數（預設 120） |
| `*_api_key` | 各 Agent 對應的 API Key（手動輸入，不存於 Secrets） |

### 本機執行

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

此專案提供 OpenCode Skills，讓你可以透過對話操作 Image 生命週期。

### 安裝 Skills

```bash
git clone https://github.com/shumingyang-opencode/dev-docker-image-packages.git
cd dev-docker-image-packages
bash skills/install.sh
```

### 可用指令

| 說 | 效果 |
|----|------|
| 「幫我安裝位在 `https://github.com/...` 的技能」 | 從 repo 安裝所有 ddip 技能 |
| 「有哪些 image」 / 「list images」 | 列出所有可用 Image |
| 「加 image」 / 「new image」 / 「create image」 | 互動式新增 Image（Dockerfile + README） |
| 「build image」 / 「建置 image」 | 觸發 GitHub Actions 建置指定 Image |

## 貢獻

歡迎提交 PR 或 Feature Request：

1. **新增 Image** — 在 `images/<name>/` 下建立 Dockerfile + 測試腳本，並在 `tests/e2e/agents/` 新增對應的設定檔
2. **改善測試** — 補強 E2E 測試案例或新增測試覆蓋範圍
3. **文件修正** — 修正錯字、補齊說明、改善文件品質

提交方式：Fork 此專案 → 開發 → 提交 PR → 我會審閱後合併

## 相關專案

- [OpenCode](https://opencode.ai) — AI 開發助手（本 Image 內建）
- [trae-agent](https://github.com/bytedance/trae-agent) — ByteDance 開源 AI Agent
- [GHCR](https://ghcr.io) — GitHub Container Registry

## License

MIT

## 專案目錄結構

```
├── docs/                    開發文件
│   └── trae-cli-auth.md           trae-cli 認證說明
├── .github/workflows/        GitHub Actions workflow
│   ├── build-image.yml           建置 + Smoke 測試
│   ├── test-image.yml            手動 Smoke 測試
│   ├── test-run-image.yml        手動 Run 測試
│   ├── test-e2e-basic.yml        E2E Basic（無需認證）
│   └── test-e2e-advanced.yml     E2E Advanced（需 API Key）
├── images/                   Docker Image 定義
│   ├── README.md                 索引（所有 Image 列表）
│   └── <name>/
│       ├── README.md             該 Image 的詳細說明
│       ├── Dockerfile            建置腳本
│       ├── test-smoke.sh         Smoke test（安裝驗證）
│       └── test-run.sh           Run test（引擎載入驗證）
├── tests/                    E2E 測試
│   └── e2e/
│       ├── conftest.py            共用 fixtures
│       ├── test_basic.py          Basic E2E（無需認證）
│       ├── test_advanced.py       Advanced E2E（需 API Key）
│       ├── agents/                各 Image 的 Agent 設定檔
│       └── README.md              E2E 測試說明
├── skills/                   OpenCode Skills
│   └── install.sh            安裝腳本
├── README.md                     繁體中文（預設）
├── README.en.md                   English
├── README.zh-CN.md                简体中文
```
