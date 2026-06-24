import json
from pathlib import Path

import yaml

from agentic_web_demo.audit import audit_events

ROOT = Path(__file__).resolve().parents[3]


def scenario_by_id(scenario_id: str) -> dict:
    suite = yaml.safe_load((ROOT / "specs" / "demo" / "evaluation-scenarios.yaml").read_text())
    return next(scenario for scenario in suite["scenarios"] if scenario["id"] == scenario_id)


def test_happy_path_evaluation_scenario(client, auth_headers):
    scenario = scenario_by_id("happy-path-literature-review")
    payload = json.loads((ROOT / "specs" / "demo" / "a2a-message-send.json").read_text())

    card = client.get("/.well-known/agent-card.json")
    response = client.post("/a2a/v1", headers=auth_headers(scenario["input"]["scopes"]), json=payload)

    assert card.status_code == 200
    assert response.status_code == 200
    result = response.json()["result"]
    assert scenario["expected"]["discoversAgentCard"] is True
    assert result["metadata"]["callsMcpTools"] == scenario["expected"]["callsMcpTools"]
    assert result["metadata"]["createsDraft"] is scenario["expected"]["createsDraft"]
    assert result["metadata"]["requiresHumanReview"] is scenario["expected"]["requiresHumanReview"]


def test_auth_denial_evaluation_scenario(client, auth_headers):
    scenario = scenario_by_id("auth-denial-missing-scope")

    response = client.post(
        "/reviews/drafts",
        headers=auth_headers(scenario["input"]["scopes"]),
        json={
            "topic": scenario["input"]["question"],
            "sourceDocumentIds": ["doc-agent-card-2025"],
            "outline": ["Discovery"],
            "humanReviewRequired": True
        }
    )

    assert response.status_code == 403
    assert response.json()["error"] == "forbidden"
    assert response.json()["missingScope"] == scenario["expected"]["missingScope"]


def test_prompt_injection_evaluation_scenario(client, auth_headers):
    scenario = scenario_by_id("prompt-injection-in-source")

    response = client.post(
        "/documents/search",
        headers=auth_headers(["research:read"]),
        json={"query": "prompt injection access tokens", "limit": 5}
    )

    assert response.status_code == 200
    incident = next(event for event in audit_events if event["event"] == "prompt_injection_detected")
    assert incident["secretDisclosure"] is scenario["expected"]["secretDisclosure"]
    assert incident["toolPolicyBypassed"] is scenario["expected"]["toolPolicyBypassed"]
    assert scenario["expected"]["incidentLogged"] is True


def test_tool_failure_evaluation_scenario(client, auth_headers):
    scenario = scenario_by_id("mcp-tool-failure")

    response = client.post(
        "/mcp",
        headers=auth_headers(["research:read"]),
        json={
            "jsonrpc": "2.0",
            "id": "tool-failure",
            "method": "tools/call",
            "params": {"name": scenario["input"]["tool"], "arguments": {"documentId": "timeout"}}
        }
    )

    assert response.status_code == 200
    data = response.json()["error"]["data"]
    assert data["retryAttempted"] is scenario["expected"]["retryAttempted"]
    assert data["userVisibleStatus"] == scenario["expected"]["userVisibleStatus"]
    assert data["createsDraft"] is scenario["expected"]["createsDraft"]


def test_stale_discovery_metadata_evaluation_scenario(client, auth_headers):
    scenario = scenario_by_id("stale-agent-card")
    payload = json.loads((ROOT / "specs" / "demo" / "a2a-message-send.json").read_text())
    payload["params"]["metadata"]["agentCardVersion"] = scenario["input"]["agentCardVersion"]

    response = client.post("/a2a/v1", headers=auth_headers(), json=payload)

    assert response.status_code == 200
    data = response.json()["error"]["data"]
    assert data["revalidatesDiscovery"] is scenario["expected"]["revalidatesDiscovery"]
    assert data["honorsCacheHeaders"] is scenario["expected"]["honorsCacheHeaders"]
    assert data["blocksUnsupportedProtocol"] is scenario["expected"]["blocksUnsupportedProtocol"]
