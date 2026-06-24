import copy
import json
from functools import lru_cache
from typing import Any

import yaml

from .paths import SPECS_DEMO_DIR


def _read_json(name: str) -> dict[str, Any]:
    return json.loads((SPECS_DEMO_DIR / name).read_text(encoding="utf-8"))


def _read_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((SPECS_DEMO_DIR / name).read_text(encoding="utf-8"))


@lru_cache
def agent_card_spec() -> dict[str, Any]:
    return _read_json("agent-card.json")


@lru_cache
def openapi_spec() -> dict[str, Any]:
    return _read_yaml("openapi.yaml")


@lru_cache
def mcp_tools_spec() -> dict[str, Any]:
    return _read_json("mcp-tools.json")


@lru_cache
def a2a_message_send_spec() -> dict[str, Any]:
    return _read_json("a2a-message-send.json")


@lru_cache
def agent_registry_spec() -> dict[str, Any]:
    return _read_yaml("agent-registry.yaml")


def local_agent_registry_entry(base_url: str, agent_id: str) -> dict[str, Any] | None:
    registry = copy.deepcopy(agent_registry_spec())
    entry = next((agent for agent in registry["agents"] if agent["id"] == agent_id), None)
    if not entry:
        return None

    entry["approvedDomain"] = base_url.removeprefix("http://").removeprefix("https://")
    entry["agentCardUrl"] = f"{base_url}/.well-known/agent-card.json"
    entry["endpoints"] = {
        "openapi": f"{base_url}/openapi.json",
        "mcp": f"{base_url}/mcp",
        "a2a": f"{base_url}/a2a/v1"
    }
    entry["registry"] = registry["registry"]
    return entry


def local_agent_card(base_url: str) -> dict[str, Any]:
    card = copy.deepcopy(agent_card_spec())
    card["url"] = f"{base_url}/a2a/v1"
    card["documentationUrl"] = f"{base_url}/openapi.json"
    card.setdefault("provider", {})["url"] = base_url
    card["securitySchemes"]["campusOidc"]["openIdConnectSecurityScheme"][
        "openIdConnectUrl"
    ] = f"{base_url}/.well-known/openid-configuration"
    return card


def local_openapi(base_url: str) -> dict[str, Any]:
    spec = copy.deepcopy(openapi_spec())
    spec["servers"] = [{"url": base_url, "description": "Local demo API origin"}]
    spec["components"]["securitySchemes"]["campusOidc"][
        "openIdConnectUrl"
    ] = f"{base_url}/.well-known/openid-configuration"
    return spec
