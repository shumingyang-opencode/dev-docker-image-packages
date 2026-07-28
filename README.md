[**繁體中文**](./README.md) · [English](./README.en.md) · [简体中文](./README.zh-CN.md)

---

# Dev Docker Image Packages

個人開發用 Docker Image 集合，透過 GitHub Actions 自動建置並發佈至 GHCR。

## 目錄

- [可用 Images](#可用-images)
- [Image Tags](#image-tags)
- [使用方式](#使用方式)
- [CI / GitHub Actions Workflows](#ci--github-actions-workflows)
- [Skills（OpenCode 整合）](#skillsopencode-整合)
- [專案目錄結構](#專案目錄結構)

---

## 可用 Images

| Image | 最新版本 | Base | 用途 | 說明文件 |
|-------|---------|------|------|---------|
| [py-devkit-image-base](./images/py-devkit-image-base/) | 1.2.0 | python:3.12-slim | Python 開發基底（含 AI CLI、trae-agent） | [README](./images/py-devkit-image-base/README.md) |

> 詳細 Image 索引請見 [images/README.md](./images/README.md)。

## Image Tags

每個 Image 發佈至 GHCR 時會標記以下 tags：

| Tag | 說明 |
|-----|------|
| `latest` | 每次 build 更新至此 tag |
| `{version}` | 同一次 build 也會更新至此 tag，兩者指向相同內容 |

建議使用 `latest` tag 取得最新版本。若需鎖定特定版本的內容，可直接使用版本 tag（如 `1.2.0`），不過每次重新建置時兩者都會同步更新。

## 使用方式

### 下載 Image

```bash
# 最新版
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:latest

# 指定版本
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:1.2.0
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
  -e GEMINI_API_KEY=your_key \
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
      - GEMINI_API_KEY=${GEMINI_API_KEY:-}
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
| **E2E 測試：進階 Prompt** (Advanced E2E) | [`test-e2e-advanced.yml`](./.github/workflows/test-e2e-advanced.yml) | 手動按鈕 | 自訂 Prompt 測試 Agent 真實回應（需 API Key） |

### 手動觸發 (gh CLI)

```bash
# 建置 + 自動測試
gh workflow run build-image.yml -f image=py-devkit-image-base
gh workflow run build-image.yml -f image=all

# Smoke 測試（驗證安裝）
gh workflow run test-image.yml -f image=py-devkit-image-base

# Run 測試（驗證引擎）
gh workflow run test-run-image.yml -f image=py-devkit-image-base

# E2E 測試
gh workflow run test-e2e-basic.yml -f image=py-devkit-image-base
gh workflow run test-e2e-advanced.yml -f image=py-devkit-image-base -f agent=opencode -f prompt="Say hello"
```

> 各 Image 的測試腳本（`test-smoke.sh` / `test-run.sh`）可獨立於 CI 在本機執行，詳見各 Image 目錄下的 README。

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

## 專案目錄結構

```
├── .github/workflows/        GitHub Actions workflow
│   ├── build-image.yml           建置 + Smoke 測試
│   ├── test-image.yml            手動 Smoke 測試
│   └── test-run-image.yml        手動 Run 測試
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
│       └── agents/                各 Image 的 Agent 設定檔
├── skills/                   OpenCode Skills
│   └── install.sh            安裝腳本
├── README.md                     繁體中文（預設）
├── README.en.md                   English
├── README.zh-CN.md                简体中文
```
