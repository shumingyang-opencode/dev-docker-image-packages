# Dev Docker Image Packages

個人開發用 Docker Image 集合，透過 GitHub Actions 自動建置並發佈至 GHCR。

## 可用 Images

| Image | 最新版本 | Base | 用途 |
|-------|---------|------|------|
| [py-devkit-image-base](./images/py-devkit-image-base/) | 1.2.0 | python:3.12-slim | Python 開發基底（含 AI CLI、trae-agent） |

完整說明請見 [images/README.md](./images/README.md)。

## Image Tags

每個 Image 發佈至 GHCR 時會標記以下 tags：

| Tag | 說明 |
|-----|------|
| `latest` | 最新穩定版本，持續更新 |
| `1.2.0` | 鎖定特定版本號，不因更新而改變 |

使用版本號 tag 確保環境一致性：

```bash
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:1.2.0
```

## 使用方式

### Pull Image

```bash
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:latest
```

### 執行容器

```bash
# 基本執行
docker run --rm -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 以 devuser 身份執行（非 root，適合安全環境）
docker run --rm --user devuser -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 掛載本機工作目錄
docker run --rm -it -v $(pwd):/workspace ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 傳遞 AI CLI 所需的 credentials
docker run --rm -it \
  -e OPENCODE_API_KEY=your_key \
  -e GEMINI_API_KEY=your_key \
  -e COPILOT_GITHUB_TOKEN=your_token \
  ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash
```

### 整合 Docker Compose

在 `docker-compose.yml` 中使用：

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

在你的 Dockerfile 中使用：

```dockerfile
FROM ghcr.io/shumingyang-opencode/py-devkit-image-base:latest

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## CI / GitHub Actions Workflows

| Workflow | 檔案 | 觸發方式 | 測試內容 |
|----------|------|---------|---------|
| 建置 · Smoke 測試 (Build + Smoke) | `build-image.yml` | 手動 + 自動 | Build → 自動 Smoke test |
| Smoke 測試：CLI 已安裝 (Install Check) | `test-image.yml` | 手動按鈕 | 驗證 binary 存在、可執行 |
| 啟動測試：CLI 可執行 (Engine Load) | `test-run-image.yml` | 手動按鈕 | 驗證 CLI 引擎能載入 |

### 手動觸發 (gh CLI)

```bash
# Build + Smoke
gh workflow run build-image.yml -f image=py-devkit-image-base

# Smoke test（指定版本驗證安裝）
gh workflow run test-image.yml -f image=py-devkit-image-base -f tag=1.2.0

# Run test（指定版本驗證引擎）
gh workflow run test-run-image.yml -f image=py-devkit-image-base -f tag=1.2.0

# 一次建置所有 Image
gh workflow run build-image.yml -f image=all
```

## Skills

與 OpenCode 搭配使用，可透過以下指令互動：

| 說 | 效果 |
|----|------|
| 「幫我安裝位在 `https://github.com/shumingyang-opencode/dev-docker-image-packages.git` 的技能」 | 從 repo 安裝所有 ddip 技能 |
| 「有哪些 image」 / 「list images」 | 列出所有可用 Image |
| 「加 image」 / 「new image」 / 「create image」 | 互動式新增 Image（Dockerfile + README） |
| 「build image」 / 「建置 image」 / 「更新 image」 | 觸發 GitHub Actions 建置指定 Image |

### 安裝 Skills

```bash
git clone https://github.com/shumingyang-opencode/dev-docker-image-packages.git
cd dev-docker-image-packages
bash skills/install.sh
```

## 目錄結構

```
├── .github/workflows/    GitHub Actions workflow
│   ├── build-image.yml       建置 + Smoke 測試
│   ├── test-image.yml        手動 Smoke 測試
│   └── test-run-image.yml    手動 Run 測試
├── images/               Docker Image 定義
│   ├── README.md         索引
│   └── <name>/
│       ├── Dockerfile        建置腳本
│       ├── README.md         說明文件
│       ├── test-smoke.sh     Smoke test 腳本（安裝驗證）
│       └── test-run.sh       Run test 腳本（引擎載入驗證）
├── skills/               OpenCode Skills
│   └── install.sh        安裝腳本
└── README.md             本檔案
```
