# python — Python 3.13 開發基底 Image

Base: `python:3.13-slim`

版本: `1.0.0`

## 功能

通用 Python 開發環境，適合 CI/CD 流程與本機開發使用。

## 預裝工具

| 類別 | 工具 | 用途 |
|------|------|------|
| 系統 | git, curl, ca-certificates, build-essential, tzdata | 版本控制、網路、編譯 |
| Python | poetry | 套件管理 |
| Python | ruff | Linter & Formatter |
| Python | mypy | 型別檢查 |
| Python | pytest | 測試框架 |

## 建議用途

- 作為其他 Docker Image 的 Base Image (`FROM ghcr.io/shumingyang-opencode/python:latest`)
- CI/CD Pipeline 中的 Python 測試與建置環境
- 本機 Python 開發容器

## 使用方式

```bash
docker pull ghcr.io/shumingyang-opencode/python:latest

# 以 devuser 身份執行
docker run --user devuser -it ghcr.io/shumingyang-opencode/python:bash
```
