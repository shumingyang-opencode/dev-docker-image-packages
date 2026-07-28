# trae-cli 認證說明

## TRAE CLI ≠ TRAE IDE

兩者是不同的產品：

| | TRAE IDE（桌面板） | trae-cli（命令列） |
|---|---|---|
| 身份 | 字節跳動的 AI IDE | 開源命令列工具（`pip install trae-agent`） |
| 認證 | 公司帳號 OAuth 登入 | 獨立的 `{PROVIDER}_API_KEY` 環境變數 |
| LLM 後端 | 公司內部服務 | 可自選 Provider |

trae-cli **無法**直接繼承 TRAE IDE 的公司帳號認證，需要額外設定 API Key。

## 支援的 Provider 與環境變數

| Provider | 環境變數 | 預設 Base URL |
|----------|---------|---------------|
| OpenRouter | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` |
| 豆包 (Doubao) | `DOUBAO_API_KEY` | `https://ark.cn-beijing.volces.com/api/v3/` |
| OpenAI | `OPENAI_API_KEY` | `https://api.openai.com/v1` |
| Anthropic | `ANTHROPIC_API_KEY` | `https://api.anthropic.com` |
| Google Gemini | `GOOGLE_API_KEY` | — |
| Azure | `AZURE_API_KEY` | — |

## 認證優先順序

```
命令列引數 > 環境變數 > 設定檔 (trae_config.yaml) > 預設值
```

## 如何取得 API Key

### OpenRouter
- 官網：https://openrouter.ai/keys
- 本機存放：`~/.local/share/opencode/auth.json`

### 豆包 (Doubao)
- 火山引擎控制台：https://console.volcengine.com/ark/region:ark+cn-zhangbei/apiKey

## 本機設定方式

### 透過環境變數（臨時）
```bash
export OPENROUTER_API_KEY=sk-or-...
trae-cli run "你的任務"
```

### 透過 trae_config.yaml（持久）
```yaml
model_providers:
  doubao:
    api_key: ${DOUBAO_API_KEY}
    base_url: https://ark.cn-beijing.volces.com/api/v3/
```

## E2E 測試對應的 Workflow 輸入欄位

| Workflow 欄位 | 對應環境變數 | Provider |
|---------------|-------------|----------|
| `openai_api_key` | `OPENAI_API_KEY` | OpenAI |
| `anthropic_api_key` | `ANTHROPIC_API_KEY` | Anthropic |
| `openrouter_api_key` | `OPENROUTER_API_KEY` | OpenRouter |
| `doubao_api_key` | `DOUBAO_API_KEY` | 豆包 |
