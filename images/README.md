# Dev Docker Images

本目錄包含所有可用的開發用 Docker Image。

| Image | 版本 | 說明 |
|-------|------|------|
| [py-devkit-image-base](./py-devkit-image-base/) | 1.2.0 | Python 3.12 開發基底，含 AI CLI / trae-agent / duckdb / poetry / ruff / mypy / pytest |

## Tags

每個 Image 在 GHCR 上提供以下 tags：

| Tag | 說明 |
|-----|------|
| `latest` | 最新穩定版本 |
| `{version}` | 鎖定特定版本（如 `1.2.0`） |

## 測試

每個 Image 目錄下包含兩個測試腳本：

| 腳本 | 用途 |
|------|------|
| `test-smoke.sh` | 驗證所有工具已安裝（binary 存在、可執行） |
| `test-run.sh` | 驗證 CLI 引擎能載入（無 auth 模式） |

對應的 GitHub Actions workflow 會自動或手動執行這些測試。

## 如何新增 Image

執行 OpenCode Skill:

> 「加 image」

或手動建立：

```bash
mkdir images/<名稱>
# 放入 Dockerfile + README.md + test-smoke.sh + test-run.sh
```

## 如何建置

執行 OpenCode Skill:

> 「build image」
