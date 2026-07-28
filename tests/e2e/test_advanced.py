import shlex
import subprocess

import pytest


def test_agent_prompt_response(container_id, selected_agent, custom_prompt, cmd_timeout):
    run_template = selected_agent.get("run_cmd")
    if not run_template:
        pytest.skip(f"No run_cmd defined for {selected_agent['name']}")

    cmd = run_template.replace("{prompt}", shlex.quote(custom_prompt))

    result = subprocess.run(
        ["docker", "exec", "-i", container_id, "bash", "-c", cmd],
        capture_output=True,
        text=True,
        timeout=cmd_timeout,
    )

    output = (result.stdout or "") + (result.stderr or "")
    print(f"\n--- {selected_agent['name']} Response (exit={result.returncode}) ---")
    print(output[:3000])
    print("--- End ---")

    assert result.returncode == 0, (
        f"Agent exited with code {result.returncode}\n"
        f"stderr: {result.stderr[:1000]}"
    )
    assert result.stdout.strip(), "Agent produced no output"
