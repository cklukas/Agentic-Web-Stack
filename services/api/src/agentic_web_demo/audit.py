import json
import logging
from datetime import UTC, datetime
from typing import Any

from .context import get_trace_id

logger = logging.getLogger("agentic_web_demo.audit")
audit_events: list[dict[str, Any]] = []

ARCHITECTURE_DEFAULTS: dict[str, dict[str, Any]] = {
    "agent_card_discovery": {"layer": "discovery", "component": "agent-card", "policyResult": "public"},
    "agent_registry_lookup": {"layer": "discovery", "component": "agent-registry", "policyResult": "approved"},
    "openapi_contract_served": {"layer": "apis", "component": "openapi", "policyResult": "public"},
    "dev_token_issued": {"layer": "identity", "component": "dev-token", "policyResult": "allowed"},
    "auth_failure": {"layer": "identity", "component": "scope-enforcement", "policyResult": "denied"},
    "documents_search": {"layer": "memory", "component": "document-search", "policyResult": "allowed"},
    "mcp_tools_list": {"layer": "agent-protocols", "component": "mcp", "policyResult": "allowed"},
    "mcp_tool_call": {"layer": "agent-protocols", "component": "mcp", "policyResult": "allowed"},
    "mcp_tool_failure": {"layer": "agent-protocols", "component": "mcp", "policyResult": "partial_result"},
    "a2a_message_send": {"layer": "agent-protocols", "component": "a2a", "policyResult": "allowed"},
    "stale_agent_card": {"layer": "discovery", "component": "agent-card", "policyResult": "denied"},
    "review_draft_created": {"layer": "applications", "component": "review-draft", "policyResult": "human_review_required"},
    "prompt_injection_detected": {"layer": "operations", "component": "evaluation", "policyResult": "blocked"}
}


def artifact_refs(fields: dict[str, Any]) -> list[str]:
    refs = list(fields.get("artifactRefs", []))

    if fields.get("draft_id"):
        refs.append(f"draft:{fields['draft_id']}")
    for document_id in fields.get("source_document_ids", []):
        refs.append(f"document:{document_id}")
    if fields.get("document_id"):
        refs.append(f"document:{fields['document_id']}")

    return refs


def audit(event: str, **fields: Any) -> dict[str, Any]:
    fields.setdefault("traceId", get_trace_id())
    for key, value in ARCHITECTURE_DEFAULTS.get(event, {}).items():
        fields.setdefault(key, value)
    refs = artifact_refs(fields)
    if refs:
        fields["artifactRefs"] = refs
    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event": event,
        **fields
    }
    audit_events.append(record)
    logger.info(json.dumps(record, sort_keys=True))
    return record


def clear_audit_events() -> None:
    audit_events.clear()


def trace_events(trace_id: str) -> list[dict[str, Any]]:
    events = [event for event in audit_events if event.get("traceId") == trace_id]
    return [
        {
            "timestamp": event["timestamp"],
            "traceId": event["traceId"],
            "event": event["event"],
            "layer": event.get("layer", "unknown"),
            "component": event.get("component", "unknown"),
            "policyResult": event.get("policyResult", "not_recorded"),
            "artifactRefs": event.get("artifactRefs", [])
        }
        for event in events
    ]
