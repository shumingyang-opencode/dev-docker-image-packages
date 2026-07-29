#!/usr/bin/env bash
# Smoke test for py-devkit-image-base
# Usage:
#   docker run --rm ghcr.io/shumingyang-opencode/py-devkit-image-base:latest \
#     bash < test-smoke.sh
#
#   # or locally if tools are installed:
#   bash test-smoke.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

total=0
passed=0
failed=0

check() {
    local name="$1"
    local cmd="$2"
    total=$((total + 1))
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} $name"
        passed=$((passed + 1))
    else
        echo -e "  ${RED}✗${NC} $name"
        failed=$((failed + 1))
    fi
}

section() {
    echo ""
    echo -e "${CYAN}--- $1 ---${NC}"
}

section "System Tools"
check "git"          "git --version"
check "node"         "node --version"
check "curl"         "curl --version"

section "Python Tools"
check "poetry"       "poetry --version"
check "ruff"         "ruff --version"
check "mypy"         "mypy --version"
check "pytest"       "pytest --version"
check "duckdb"       "python -c 'import duckdb; print(duckdb.__version__)'"

section "AI CLIs"
check "opencode"     "opencode --version"
check "copilot"      "copilot --help"
check "lark-cli"     "lark-cli --version"
check "trae-cli(bin)" "command -v trae-cli"
check "trae-cli(mod)" "python -c 'from trae_agent.cli import cli'"

echo ""
echo "================================"
echo -e "  Result: ${GREEN}$passed passed${NC}, ${RED}$failed failed${NC} (14 total)"
echo "================================"

if [ "$failed" -gt 0 ]; then
    exit 1
fi
