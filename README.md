# Dev Docker Image Packages

個人開發用 Docker Image 集合，透過 GitHub Actions 自動建置並發佈至 GHCR。

## 可用 Images

| Image | 版本 | Base | 用途 |
|-------|------|------|------|
| [py-devkit-image-base](./images/py-devkit-image-base/) | 1.2.0 | python:3.12-slim | Python 開發基底（含 AI CLI、trae-agent） |

完整說明請見 [images/README.md](./images/README.md)。

## 使用方式

### Pull Image

```bash
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:latest
```

### 執行容器

```bash
# 基本執行
docker run --rm -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 以 devuser 身份執行
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

### 作為 Base Image

在你的 Dockerfile 中使用：

```dockerfile
FROM ghcr.io/shumingyang-opencode/py-devkit-image-base:latest

# 你的應用層
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## CI / GitHub Actions Workflows

| Workflow | 觸發方式 | 測試內容 |
|----------|---------|---------|
| 建置 · Smoke 測試 (Build + Smoke) | 手動 + 自動（每次 build） | **Build image → 自動執行 Smoke test**，驗證所有工具已安裝 |
| Smoke 測試：CLI 已安裝 (Install Check) | 手動按鈕 | 對已 publish 的任一版本執行 **Smoke test**（binary 存在、可執行） |
| 啟動測試：CLI 可執行 (Engine Load) | 手動按鈕 | 對已 publish 的任一版本執行 **Run test**（CLI 引擎能載入、給出正確錯誤） |

### 手動觸發 Build

前往 GitHub → Actions → 建置 · Smoke 測試 (Build + Smoke) → Run workflow

或使用 gh CLI：

```bash
gh workflow run build-image.yml -f image=py-devkit-image-base
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
