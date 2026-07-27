# py-devkit-image-base — Python 開發工具包基底 Image

Base: `python:3.12-slim`

版本: `1.2.0`

## 功能

通用 Python 開發環境，內建 AI CLI 工具集，適合 CI/CD 流程與本機開發使用。

## 預裝工具

| 類別 | 工具 | Binary | 用途 |
|------|------|--------|------|
| 系統 | git, curl, ca-certificates, build-essential, tzdata, sqlite3 | — | 版本控制、網路、編譯、資料庫 |
| 系統 | fonts-noto-cjk | — | 中文字型支援 |
| 系統 | Node.js 22 | node | JavaScript runtime |
| Python | poetry | poetry | 套件管理 |
| Python | ruff | ruff | Linter & Formatter |
| Python | mypy | mypy | 型別檢查 |
| Python | pytest | pytest | 測試框架 |
| Python | duckdb | duckdb (Python library) | 嵌入式 SQL OLAP 資料庫 |
| AI CLI | OpenCode | `opencode` | AI 開發助手 |
| AI CLI | GitHub Copilot | `copilot` | AI Code Agent |
| AI CLI | Google Gemini CLI | `gemini` | AI 開發助手 |
| AI CLI | Lark CLI | `lark-cli` | 飛書開發工具 |
| AI CLI | Trae Agent | `trae-cli` | AI Code Agent |

### AI CLI 認證方式

各 CLI 可透過環境變數傳遞 credentials：

| CLI | Environment Variable |
|-----|---------------------|
| opencode | `OPENCODE_API_KEY` |
| copilot | `COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN` |
| gemini | `GEMINI_API_KEY` / `GOOGLE_GENAI_USE_VERTEXAI` |
| lark-cli | 執行 `lark-cli config init --new` 互動式認證 |
| trae-cli | `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`（依 provider） |

## 建議用途

- 作為其他 Docker Image 的 Base Image
- CI/CD Pipeline 中的 Python 測試與建置環境
- 本機 Python 開發容器（含 AI CLI 輔助）

## 使用方式

### Pull Image

```bash
# 最新版本
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:latest

# 鎖定特定版本
docker pull ghcr.io/shumingyang-opencode/py-devkit-image-base:1.2.0
```

### 執行容器

```bash
# 進入互動式 Shell
docker run --rm -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 以 devuser 身份執行（非 root）
docker run --rm --user devuser -it ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 掛載本機專案目錄
docker run --rm -it -v $(pwd):/workspace ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash

# 傳遞 API Key（給 AI CLI 使用）
docker run --rm -it \
  -e OPENCODE_API_KEY=your_key \
  -e GEMINI_API_KEY=your_key \
  -e COPILOT_GITHUB_TOKEN=your_token \
  -v $(pwd):/workspace \
  ghcr.io/shumingyang-opencode/py-devkit-image-base:latest bash
```

### 作為 Base Image

```dockerfile
FROM ghcr.io/shumingyang-opencode/py-devkit-image-base:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## 測試

本 Image 提供兩個測試腳本，可獨立執行：

### Smoke Test — 驗證工具已安裝

確認所有 binary 存在於 PATH 且可執行 `--version` / `--help`：

```bash
docker run --rm ghcr.io/shumingyang-opencode/py-devkit-image-base:latest \
  bash < images/py-devkit-image-base/test-smoke.sh
```

預期結果：15 passed, 0 failed

### Run Test — 驗證 CLI 引擎能載入

在不提供 credentials 的情況下，確認每個 CLI 能正確載入引擎並給出可預期的錯誤訊息：

```bash
docker run --rm -i ghcr.io/shumingyang-opencode/py-devkit-image-base:latest \
  bash < images/py-devkit-image-base/test-run.sh
```

預期結果：5 passed, 0 failed
