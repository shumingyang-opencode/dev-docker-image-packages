import os
import subprocess
from pathlib import Path

import pytest
import yaml


def pytest_addoption(parser):
    parser.addoption("--image", action="store", required=True)
    parser.addoption("--tag", action="store", default="latest")
    parser.addoption("--agent", action="store", default=None)
    parser.addoption("--prompt", action="store", default=None)
    parser.addoption("--timeout", action="store", type=int, default=120)
    parser.addoption("--model", action="store", default="default")


def load_agent_config(image_name):
    config_path = Path(__file__).parent / "agents" / f"{image_name}.yaml"
    if not config_path.exists():
        pytest.fail(f"Agent config not found: {config_path}")
    with open(config_path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def image_name(request):
    return request.config.getoption("--image")


@pytest.fixture(scope="session")
def agent_config(image_name):
    return load_agent_config(image_name)


@pytest.fixture(scope="session")
def image_tag(request):
    return request.config.getoption("--tag")


@pytest.fixture(scope="session")
def ghcr_full_tag(agent_config, image_tag):
    return f"{agent_config['ghcr_repo']}:{image_tag}"


@pytest.fixture(scope="session")
def pull_image(ghcr_full_tag):
    subprocess.run(["docker", "pull", ghcr_full_tag], check=True, capture_output=True)
    return ghcr_full_tag


@pytest.fixture(scope="module")
def selected_agent(request, agent_config):
    agent_name = request.config.getoption("--agent")
    if not agent_name:
        pytest.skip("No agent specified (use --agent)")
    for agent in agent_config["agents"]:
        if agent["name"] == agent_name:
            return agent
    pytest.fail(f"Agent '{agent_name}' not found in config")


@pytest.fixture(scope="module")
def custom_prompt(request):
    return request.config.getoption("--prompt") or "Say hello and introduce yourself briefly."


@pytest.fixture(scope="module")
def cmd_timeout(request):
    return request.config.getoption("--timeout")


@pytest.fixture(scope="module")
def llm_model(request):
    return request.config.getoption("--model")


@pytest.fixture(scope="module")
def check_env_vars(selected_agent):
    missing = [v for v in selected_agent.get("env_vars", []) if v not in os.environ]
    if missing:
        pytest.skip(f"Required env vars not set: {', '.join(missing)}")


@pytest.fixture(scope="module")
def container_id(check_env_vars, pull_image, selected_agent):
    cmd = ["docker", "run", "-d", "-i", "--init"]
    for var_name in selected_agent.get("env_vars", []):
        if var_name in os.environ:
            cmd.extend(["-e", var_name])
    cmd.append(pull_image)
    cmd.append("sleep")
    cmd.append("infinity")

    cid = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
    try:
        yield cid
    finally:
        subprocess.run(["docker", "rm", "-f", cid], capture_output=True)
