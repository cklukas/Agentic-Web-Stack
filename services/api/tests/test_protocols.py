import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def test_mcp_tools_list_and_tool_calls(client, auth_headers):
    headers = auth_headers(["research:read"])

    tools = client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert tools.status_code == 200
    assert [tool["name"] for tool in tools.json()["result"]["tools"]] == ["search_documents", "fetch_document"]

    search = client.post(
        "/mcp",
        headers=headers,
        json={
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "search_documents", "arguments": {"query": "mcp tools", "limit": 3}}
        }
    )
    assert search.status_code == 200
    assert search.json()["result"]["content"][0]["json"]["results"]

    fetch = client.post(
        "/mcp",
        headers=headers,
        json={
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "fetch_document", "arguments": {"documentId": "doc-mcp-2024"}}
        }
    )
    assert fetch.status_code == 200
    assert fetch.json()["result"]["content"][0]["json"]["title"] == "Model Context Protocol for Tool and Resource Access"


def test_mcp_unknown_tool_and_malformed_request(client, auth_headers):
    headers = auth_headers(["research:read"])

    unknown = client.post(
        "/mcp",
        headers=headers,
        json={"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "unknown"}}
    )
    assert unknown.status_code == 200
    assert unknown.json()["error"]["code"] == -32601

    malformed = client.post("/mcp", headers=headers, json={"method": "tools/list"})
    assert malformed.status_code == 400
    assert malformed.json()["error"] == "invalid_json_rpc"


def test_a2a_message_send_happy_path(client, auth_headers):
    payload = json.loads((ROOT / "specs" / "demo" / "a2a-message-send.json").read_text())

    response = client.post("/a2a/v1", headers=auth_headers(), json=payload)

    assert response.status_code == 200
    result = response.json()["result"]
    assert result["status"]["state"] == "completed"
    assert result["metadata"]["callsMcpTools"] == ["search_documents", "fetch_document"]
    assert result["metadata"]["createsDraft"] is True
    assert result["metadata"]["requiresHumanReview"] is True
    assert result["artifacts"][0]["parts"][0]["data"]["citations"]


def test_a2a_missing_scope_metadata_unsupported_method_and_malformed_request(client, auth_headers):
    payload = json.loads((ROOT / "specs" / "demo" / "a2a-message-send.json").read_text())
    payload["params"]["metadata"].pop("requiredScopes")

    missing_metadata = client.post("/a2a/v1", headers=auth_headers(), json=payload)
    assert missing_metadata.status_code == 200
    assert missing_metadata.json()["error"]["data"]["errorCategory"] == "missing_scope_metadata"

    unsupported = client.post(
        "/a2a/v1",
        headers=auth_headers(),
        json={"jsonrpc": "2.0", "id": "bad", "method": "tasks/get", "params": {}}
    )
    assert unsupported.status_code == 200
    assert unsupported.json()["error"]["code"] == -32601

    malformed = client.post("/a2a/v1", headers=auth_headers(), json={"method": "message/send"})
    assert malformed.status_code == 400
    assert malformed.json()["error"] == "invalid_json_rpc"
