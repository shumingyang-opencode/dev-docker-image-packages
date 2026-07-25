# Dev Docker Images

本目錄包含所有可用的開發用 Docker Image。

| Image | 版本 | 說明 |
|-------|------|------|
| [py-devkit-image-base](./py-devkit-image-base/) | 1.1.0 | Python 3.13 開發基底，含 AI CLI / duckdb / poetry / ruff / mypy / pytest |

## 如何新增 Image

執行 OpenCode Skill:

> 「加 image」

或手動建立：

```bash
mkdir images/<名稱>
# 放入 Dockerfile + README.md
```

## 如何建置

執行 OpenCode Skill:

> 「build image」
