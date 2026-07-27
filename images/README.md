# Dev Docker Images

本目錄包含所有可用的開發用 Docker Image。

> 🔙 [專案根目錄](../README.md) — 快速開始、下載方式、CI 說明

| Image | 版本 | Base | 預裝工具 | 詳細說明 |
|-------|------|------|---------|---------|
| [py-devkit-image-base](./py-devkit-image-base/) | 1.2.0 | python:3.12-slim | AI CLI × 5, poetry, ruff, pytest, duckdb | [README](./py-devkit-image-base/README.md) |

## Tags

每個 Image 在 GHCR 上提供以下 tags：

| Tag | 說明 |
|-----|------|
| `latest` | 每次 build 更新至此 tag |
| `{version}` | 同一次 build 也會更新至此 tag，兩者指向相同內容 |

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

或使用 gh CLI：

```bash
gh workflow run build-image.yml -f image=py-devkit-image-base
```
