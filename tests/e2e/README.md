# E2E Tests

End-to-end tests for Docker images. Tests pull images from GHCR and verify agents work correctly.

## Structure

```
tests/e2e/
├── conftest.py               # Shared fixtures: YAML loading, Docker lifecycle
├── test_basic.py             # Basic E2E tests (no auth needed)
├── test_advanced.py          # Advanced E2E tests (needs API keys)
├── agents/                   # Per-image agent configuration
│   └── py-devkit-image-base.yaml
└── README.md
```

## Running Locally

### Basic Tests

```bash
# Test a single image
pytest tests/e2e/test_basic.py --image py-devkit-image-base --tag latest -v
```

### Advanced Tests (needs API keys)

```bash
export OPENCODE_API_KEY=sk-...
pytest tests/e2e/test_advanced.py \
  --image py-devkit-image-base \
  --tag latest \
  --agent opencode \
  --prompt "Say hello" \
  --timeout 120 \
  -v
```

## Adding a New Image

1. Create `tests/e2e/agents/<image-name>.yaml` defining the agents to test
2. Add the image name to the `options` list in `.github/workflows/test-e2e-basic.yml` and `test-e2e-advanced.yml`
