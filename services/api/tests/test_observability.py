from agentic_web_demo.audit import audit_events


def test_trace_id_is_propagated_to_response_and_audit_events(client, auth_headers):
    trace_id = "trace-test-observability"
    response = client.post(
        "/documents/search",
        headers={**auth_headers(["research:read"]), "X-Trace-Id": trace_id},
        json={"query": "agent interoperability protocols", "limit": 2}
    )

    assert response.status_code == 200
    assert response.headers["x-trace-id"] == trace_id
    assert any(event["event"] == "documents_search" and event["traceId"] == trace_id for event in audit_events)


def test_json_rpc_responses_include_trace_metadata(client, auth_headers):
    trace_id = "trace-json-rpc-test"
    response = client.post(
        "/mcp",
        headers={**auth_headers(["research:read"]), "X-Trace-Id": trace_id},
        json={"jsonrpc": "2.0", "id": "tools", "method": "tools/list"}
    )

    assert response.status_code == 200
    assert response.json()["meta"]["traceId"] == trace_id
    assert response.headers["x-trace-id"] == trace_id


def test_debug_runtime_requires_debug_scope_and_returns_metadata(client, auth_headers):
    missing_token = client.get("/debug/runtime")
    assert missing_token.status_code == 401

    missing_scope = client.get("/debug/runtime", headers=auth_headers(["research:read"]))
    assert missing_scope.status_code == 403
    assert missing_scope.json()["missingScope"] == "debug:read"

    response = client.get("/debug/runtime", headers=auth_headers(["debug:read"]))
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "literature-review-assistant"
    assert data["corpusCount"] >= 5
    assert "debug:read" in data["supportedScopes"]
    assert data["specs"]["agentCardVersion"] == "0.2.0"
    assert data["specs"]["a2aMethod"] == "message/send"


def test_debug_audit_events_returns_recent_events_without_tokens(client, auth_headers):
    trace_id = "trace-audit-read"
    client.post(
        "/documents/search",
        headers={**auth_headers(["research:read"]), "X-Trace-Id": trace_id},
        json={"query": "mcp tools", "limit": 1}
    )

    response = client.get("/debug/audit-events", headers=auth_headers(["debug:read"]), params={"limit": 5})

    assert response.status_code == 200
    events = response.json()["events"]
    assert any(event["event"] == "documents_search" and event["traceId"] == trace_id for event in events)
    assert "access_token" not in str(events)


def test_debug_trace_requires_debug_scope_and_returns_safe_architecture_events(client, auth_headers):
    trace_id = "trace-architecture-test"
    client.get("/.well-known/agent-card.json", headers={"X-Trace-Id": trace_id})
    client.get("/registry/agents/literature-review-assistant", headers={"X-Trace-Id": trace_id})
    client.post(
        "/documents/search",
        headers={**auth_headers(["research:read"]), "X-Trace-Id": trace_id},
        json={"query": "agent interoperability protocols", "limit": 1}
    )

    missing_token = client.get(f"/debug/traces/{trace_id}")
    assert missing_token.status_code == 401

    missing_scope = client.get(f"/debug/traces/{trace_id}", headers=auth_headers(["research:read"]))
    assert missing_scope.status_code == 403
    assert missing_scope.json()["missingScope"] == "debug:read"

    response = client.get(f"/debug/traces/{trace_id}", headers=auth_headers(["debug:read"]))
    assert response.status_code == 200
    events = response.json()["events"]
    assert [event["event"] for event in events[:2]] == ["agent_card_discovery", "agent_registry_lookup"]
    assert all({"traceId", "event", "layer", "component", "policyResult", "artifactRefs"} <= set(event) for event in events)
    assert any(event["component"] == "agent-registry" and event["policyResult"] == "approved" for event in events)
    assert "access_token" not in str(events)
    assert "Bearer" not in str(events)


def test_dev_token_rejects_unsupported_scopes(client):
    response = client.get("/auth/dev-token", params={"scope": "admin:all"})

    assert response.status_code == 400
    assert response.json()["error"] == "unsupported_scope"
