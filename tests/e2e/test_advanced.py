import shlex
import subprocess

import pytest


def test_agent_prompt_response(container_id, selected_agent, custom_prompt, cmd_timeout, llm_model):
    run_template = selected_agent.get("run_cmd")
    if not run_template:
        pytest.skip(f"No run_cmd defined for {selected_agent['name']}")

    cmd = run_template.replace("{prompt}", shlex.quote(custom_prompt))
    if selected_agent.get("supports_model") and llm_model and llm_model != "default":
        cmd += f" --model {shlex.quote(llm_model)}"

    proc = subprocess.Popen(
        ["docker", "exec", "-i", container_id, "bash", "-c", cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=cmd_timeout)
        returncode = proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        returncode = -1

    output = (stdout or "") + (stderr or "")
    print(f"\n--- {selected_agent['name']} Response (exit={returncode}) ---")
    print(output[:3000])
    print("--- End ---")

    if returncode == -1:
        pytest.fail(
            f"Agent timed out after {cmd_timeout}s\n"
            f"partial output: {output[:1000]}"
        )
    assert returncode == 0, (
        f"Agent exited with code {returncode}\n"
        f"stderr: {stderr[:1000]}"
    )
    assert stdout.strip(), "Agent produced no output"
