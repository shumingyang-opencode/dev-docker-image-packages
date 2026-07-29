#!/usr/bin/env bash
# No-auth run tests for py-devkit-image-base
# Verifies each AI CLI loads correctly and gives expected auth error.
# Usage:
#   docker run --rm -i ghcr.io/shumingyang-opencode/py-devkit-image-base:latest \
#     bash < test-run.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

total=0
passed=0
failed=0

check_run() {
    local name="$1"
    local cmd="$2"
    local expected_exit="$3"
    local expected_msg="$4"
    total=$((total + 1))

    local exit_code
    local output_file
    output_file=$(mktemp)

    timeout 15 bash -c "$cmd" < /dev/null > "$output_file" 2>&1 && exit_code=0 || exit_code=$?

    local output
    output=$(cat "$output_file")
    rm -f "$output_file"

    if [ "$exit_code" -eq 124 ]; then
        echo -e "  ${RED}✗${NC} $name (timed out)"
        failed=$((failed + 1))
        return
    fi

    if [ "$exit_code" -ne "$expected_exit" ]; then
        echo -e "  ${RED}✗${NC} $name (expected exit $expected_exit, got $exit_code)"
        echo "       output: $(echo "$output" | head -20 | tr '\n' ';')"
        failed=$((failed + 1))
        return
    fi

    if ! echo "$output" | grep -qiF "$expected_msg"; then
        echo -e "  ${RED}✗${NC} $name (expected message \"$expected_msg\")"
        echo "       output: $(echo "$output" | head -20 | tr '\n' ';')"
        failed=$((failed + 1))
        return
    fi

    echo -e "  ${GREEN}✓${NC} $name"
    passed=$((passed + 1))
}

section() {
    echo ""
    echo -e "${CYAN}--- $1 ---${NC}"
}

echo "=== CLI Run Tests (no-auth) ==="

section "AI CLIs"
check_run "opencode"     "opencode run 'test' --attach http://localhost:1"               1 "Session not found"
check_run "copilot"      "echo 'hi' | copilot"                                          1 "No authentication"
check_run "lark-cli"     "lark-cli whoami"                                              3 "not configured"
check_run "trae-cli"     "python -c 'from trae_agent.cli import cli; print(\"Trae CLI OK\")'" 0 "Trae CLI OK"

echo ""
echo "================================"
echo -e "  Result: ${GREEN}$passed passed${NC}, ${RED}$failed failed${NC} ($total total)"
echo "================================"

if [ "$failed" -gt 0 ]; then
    exit 1
fi
