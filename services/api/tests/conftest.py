import pytest
from fastapi.testclient import TestClient

from agentic_web_demo.audit import clear_audit_events
from agentic_web_demo.main import app


@pytest.fixture(autouse=True)
def reset_audit_events():
    clear_audit_events()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_headers(client: TestClient):
    def factory(scopes: list[str] | None = None) -> dict[str, str]:
        effective_scopes = scopes or ["research:read", "drafts:write"]
        response = client.get("/auth/dev-token", params=[("scope", scope) for scope in effective_scopes])
        assert response.status_code == 200
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return factory
