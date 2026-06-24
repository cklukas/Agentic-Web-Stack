from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_agent_card_is_localized_and_cacheable(client):
    source = yaml.safe_load((ROOT / "specs" / "demo" / "openapi.yaml").read_text())

    response = client.get("/.well-known/agent-card.json")

    assert response.status_code == 200
    assert response.json()["name"] == "Literature Review Assistant"
    assert response.json()["url"] == "http://testserver/a2a/v1"
    assert response.headers["cache-control"] == "public, max-age=60"
    assert source["info"]["version"] == response.json()["version"]

    cached = client.get("/.well-known/agent-card.json", headers={"If-None-Match": response.headers["etag"]})
    assert cached.status_code == 304


def test_openapi_is_served_from_canonical_spec_with_local_server(client):
    canonical = yaml.safe_load((ROOT / "specs" / "demo" / "openapi.yaml").read_text())

    response = client.get("/openapi.json")

    assert response.status_code == 200
    spec = response.json()
    assert spec["info"]["title"] == canonical["info"]["title"]
    assert spec["servers"][0]["url"] == "http://testserver"
    assert spec["paths"]["/documents/search"]["post"]["operationId"] == "searchDocuments"
    assert spec["paths"]["/reviews/drafts"]["post"]["operationId"] == "createReviewDraft"


def test_agent_registry_entry_is_localized_and_unknown_agents_404(client):
    response = client.get("/registry/agents/literature-review-assistant")

    assert response.status_code == 200
    entry = response.json()
    assert entry["id"] == "literature-review-assistant"
    assert entry["trustLevel"] == "organization-approved"
    assert entry["agentCardUrl"] == "http://testserver/.well-known/agent-card.json"
    assert entry["endpoints"]["a2a"] == "http://testserver/a2a/v1"
    assert entry["registry"]["version"] == "0.1.0"

    missing = client.get("/registry/agents/unknown-agent")
    assert missing.status_code == 404
    assert missing.json()["error"] == "not_found"


def test_search_happy_path_year_filter_limit_and_empty_results(client, auth_headers):
    headers = auth_headers(["research:read"])

    response = client.post(
        "/documents/search",
        headers=headers,
        json={"query": "agent interoperability protocols", "yearFrom": 2023, "limit": 2}
    )

    assert response.status_code == 200
    results = response.json()["results"]
    assert 1 <= len(results) <= 2
    assert results[0]["documentId"].startswith("doc-")
    assert "score" in results[0]

    empty = client.post(
        "/documents/search",
        headers=headers,
        json={"query": "oauth2", "yearFrom": 2023, "limit": 5}
    )
    assert empty.status_code == 200
    assert empty.json()["results"] == []


def test_document_retrieval_success_and_not_found(client, auth_headers):
    headers = auth_headers(["research:read"])

    response = client.get("/documents/doc-a2a-2025", headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Agent2Agent Communication for Delegated Tasks"

    missing = client.get("/documents/missing", headers=headers)
    assert missing.status_code == 404
    assert missing.json()["error"] == "not_found"


def test_draft_creation_success_and_invalid_source_ids(client, auth_headers):
    headers = auth_headers(["drafts:write"])

    response = client.post(
        "/reviews/drafts",
        headers=headers,
        json={
            "topic": "Agent interoperability protocols",
            "sourceDocumentIds": ["doc-agent-card-2025", "doc-a2a-2025"],
            "outline": ["Discovery", "Delegation"],
            "humanReviewRequired": True
        }
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pending_review"
    assert response.json()["reviewUrl"].startswith("http://testserver/reviews/drafts/")

    invalid = client.post(
        "/reviews/drafts",
        headers=headers,
        json={
            "topic": "Invalid sources",
            "sourceDocumentIds": ["missing"],
            "outline": ["One"],
            "humanReviewRequired": True
        }
    )
    assert invalid.status_code == 400
    assert invalid.json()["error"] == "invalid_source_documents"


def test_draft_creation_requires_token_and_scope(client, auth_headers):
    payload = {
        "topic": "Agent interoperability protocols",
        "sourceDocumentIds": ["doc-agent-card-2025"],
        "outline": ["Discovery"],
        "humanReviewRequired": True
    }

    missing_token = client.post("/reviews/drafts", json=payload)
    assert missing_token.status_code == 401
    assert missing_token.json()["error"] == "unauthorized"

    missing_scope = client.post("/reviews/drafts", headers=auth_headers(["research:read"]), json=payload)
    assert missing_scope.status_code == 403
    assert missing_scope.json()["missingScope"] == "drafts:write"
