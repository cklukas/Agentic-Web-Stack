import json
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[3]


def wait_for_health(base_url: str, process: subprocess.Popen, timeout: float = 10.0) -> None:
    started_at = time.monotonic()
    while time.monotonic() - started_at < timeout:
        if process.poll() is not None:
            stdout, stderr = process.communicate(timeout=1)
            raise AssertionError(f"API process exited early\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        try:
            response = httpx.get(f"{base_url}/health", timeout=0.5)
            if response.status_code == 200:
                return
        except httpx.HTTPError:
            time.sleep(0.2)
    raise AssertionError(f"Timed out waiting for {base_url}/health")


def start_api(port: int) -> subprocess.Popen:
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "--app-dir",
            str(ROOT / "services/api/src"),
            "agentic_web_demo.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port)
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


def stop_process(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def test_run_demo_fails_when_api_is_unavailable():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "examples/literature-review/run_demo.py"),
            "--base-url",
            "http://127.0.0.1:9",
            "--json"
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result.returncode == 1
    assert "Could not connect" in result.stderr


def test_run_demo_supports_custom_query_json_and_audit_output(free_tcp_port):
    base_url = f"http://127.0.0.1:{free_tcp_port}"
    process = start_api(free_tcp_port)
    try:
        wait_for_health(base_url, process)
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "examples/literature-review/run_demo.py"),
                "--base-url",
                base_url,
                "--query",
                "prompt injection access tokens",
                "--show-audit",
                "--json"
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20
        )
    finally:
        stop_process(process)

    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["query"] == "prompt injection access tokens"
    assert summary["a2aTaskState"] == "completed"
    assert summary["traceId"] == "trace-demo-001"
    assert any(event["event"] == "prompt_injection_detected" for event in summary["auditEvents"])


def test_run_demo_supports_architecture_trace_output(free_tcp_port):
    base_url = f"http://127.0.0.1:{free_tcp_port}"
    process = start_api(free_tcp_port)
    try:
        wait_for_health(base_url, process)
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "examples/literature-review/run_demo.py"),
                "--base-url",
                base_url,
                "--show-trace",
                "--json"
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20
        )
    finally:
        stop_process(process)

    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["registryTrustLevel"] == "organization-approved"
    assert any(event["component"] == "agent-registry" for event in summary["trace"])
    assert any(event["layer"] == "agent-protocols" for event in summary["trace"])
    assert "access_token" not in result.stdout


def test_demo_doctor_can_pass_and_report_missing_files():
    env = {
        **os.environ,
        "DEMO_DOCTOR_COMMANDS": "node --version",
        "DEMO_DOCTOR_REQUIRED_FILES": "package.json",
        "DEMO_DOCTOR_PORT": "0"
    }
    passing = subprocess.run(
        ["node", "scripts/demo-doctor.mjs"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=10
    )
    assert passing.returncode == 0
    assert "Demo doctor checks passed" in passing.stdout

    failing = subprocess.run(
        ["node", "scripts/demo-doctor.mjs"],
        cwd=ROOT,
        env={**env, "DEMO_DOCTOR_REQUIRED_FILES": "missing.file"},
        capture_output=True,
        text=True,
        timeout=10
    )
    assert failing.returncode == 1
    assert "[fail] file missing.file" in failing.stdout


def test_demo_smoke_script_successfully_runs_workflow():
    result = subprocess.run(
        ["node", "scripts/demo-smoke.mjs"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30
    )

    assert result.returncode == 0, result.stderr
    assert "Demo smoke check passed" in result.stdout
    assert "trace-demo-001" in result.stdout


def test_demo_smoke_reports_api_startup_failure():
    result = subprocess.run(
        ["node", "scripts/demo-smoke.mjs"],
        cwd=ROOT,
        env={**os.environ, "DEMO_SMOKE_APP": "missing:app", "DEMO_SMOKE_TIMEOUT_MS": "2000"},
        capture_output=True,
        text=True,
        timeout=15
    )

    assert result.returncode == 1
    assert "API process exited before /health became ready" in result.stderr
