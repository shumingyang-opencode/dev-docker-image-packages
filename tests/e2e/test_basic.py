import subprocess


def pytest_generate_tests(metafunc):
    if "agent" in metafunc.fixturenames:
        from conftest import load_agent_config

        config = load_agent_config(metafunc.config.getoption("--image"))
        metafunc.parametrize(
            "agent",
            config["agents"],
            ids=[a["name"] for a in config["agents"]],
        )


def test_agent_executable(agent, pull_image):
    binary = agent["binary"]
    result = subprocess.run(
        [
            "docker", "run", "--rm", pull_image,
            "bash", "-c",
            f"command -v {binary} && {{ {binary} --version 2>/dev/null || {binary} --help 2>/dev/null; }}",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"{agent['name']}: binary '{binary}' check failed\n"
        f"stderr: {result.stderr[:300]}"
    )
