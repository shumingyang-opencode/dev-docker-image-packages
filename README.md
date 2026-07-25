# Dev Docker Image Packages

個人開發用 Docker Image 集合，透過 GitHub Actions 自動建置並發佈至 GHCR。

## 可用 Images

| Image | 版本 | 用途 |
|-------|------|------|
| [py-devkit-image-base](./images/py-devkit-image-base/) | 1.1.0 | Python 3.13 開發基底（含 AI CLI、duckdb） |

完整說明請見 [images/README.md](./images/README.md)。

## 快速開始

### 1. 安裝 Skills

```bash
git clone https://github.com/shumingyang-opencode/dev-docker-image-packages.git
cd dev-docker-image-packages
bash skills/install.sh
```

或對 OpenCode 說：

> 「幫我安裝位在 `https://github.com/shumingyang-opencode/dev-docker-image-packages.git` 的技能」
> 或簡單說：「安裝技能」

### 2. 可用指令

| 說 | 效果 |
|----|------|
| 「幫我安裝位在 `https://github.com/shumingyang-opencode/dev-docker-image-packages.git` 的技能」 | 從 repo 安裝所有 ddip 技能 |
| 「有哪些 image」 / 「list images」 / 「可用 image」 | 列出所有可用 Image |
| 「加 image」 / 「new image」 / 「create image」 | 互動式新增 Image（Dockerfile + README） |
| 「build image」 / 「建置 image」 / 「更新 image」 | 觸發 GitHub Actions 建置指定 Image |

### 3. 手動觸發 Build

前往 GitHub → Actions → Build Docker Image → Run workflow

或使用 gh CLI：

```bash
gh workflow run build-image.yml -f image=py-devkit-image-base
gh workflow run build-image.yml -f image=all
```

### 4. Pull Image

```bash
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:latest
```

## 目錄結構

```
├── .github/workflows/    GitHub Actions workflow
├── images/               Docker Image 定義
│   ├── README.md         索引
│   └── <name>/
│       ├── Dockerfile    建置腳本
│       └── README.md     說明文件
├── skills/               OpenCode Skills
│   └── install.sh        安裝腳本
└── README.md             本檔案
```
