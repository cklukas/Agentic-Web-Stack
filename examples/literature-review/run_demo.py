import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import httpx

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_QUERY = "agent interoperability protocols"
DEFAULT_TRACE_ID = "trace-demo-001"


def load_a2a_payload() -> dict[str, Any]:
    return json.loads((REPOSITORY_ROOT / "specs" / "demo" / "a2a-message-send.json").read_text())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Literature Review Assistant demo workflow.")
    parser.add_argument("--base-url", default=os.environ.get("DEMO_API_URL", DEFAULT_BASE_URL))
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--json", action="store_true", help="Print compact JSON only.")
    parser.add_argument("--show-audit", action="store_true", help="Include recent audit events in the summary.")
    parser.add_argument("--show-trace", action="store_true", help="Include the ordered architecture trace in the summary.")
    return parser.parse_args()


def checked(response: httpx.Response) -> httpx.Response:
    response.raise_for_status()
    return response


def require_json_rpc_result(payload: dict[str, Any], step: str) -> dict[str, Any]:
    if "error" in payload:
        raise RuntimeError(f"{step} returned JSON-RPC error: {json.dumps(payload['error'], sort_keys=True)}")
    if "result" not in payload:
        raise RuntimeError(f"{step} did not return a JSON-RPC result.")
    return payload["result"]


def token(client: httpx.Client, scopes: list[str]) -> str:
    response = checked(
        client.get(
            "/auth/dev-token",
            params=[("scope", scope) for scope in scopes],
            headers={"X-Trace-Id": DEFAULT_TRACE_ID}
        )
    ).json()
    return response["access_token"]


def update_a2a_question(payload: dict[str, Any], query: str) -> dict[str, Any]:
    parts = payload["params"]["message"]["parts"]
    for part in parts:
        if part.get("kind") == "text":
            part["text"] = (
                f"Find recent papers about {query}, compare the main protocol approaches, "
                "and return a cited literature review outline."
            )
            break
    payload["params"]["metadata"]["traceId"] = DEFAULT_TRACE_ID
    return payload


def run_workflow(base_url: str, query: str, show_audit: bool, show_trace: bool) -> dict[str, Any]:
    scopes = ["research:read", "drafts:write"]
    if show_audit or show_trace:
        scopes.append("debug:read")

    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        access_token = token(client, scopes)
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Trace-Id": DEFAULT_TRACE_ID
        }

        agent_card = checked(client.get("/.well-known/agent-card.json", headers={"X-Trace-Id": DEFAULT_TRACE_ID})).json()
        registry_entry = checked(
            client.get("/registry/agents/literature-review-assistant", headers={"X-Trace-Id": DEFAULT_TRACE_ID})
        ).json()
        search_response = checked(
            client.post(
                "/documents/search",
                headers=headers,
                json={
                    "query": query,
                    "yearFrom": 2023,
                    "limit": 5
                }
            )
        ).json()
        search_results = search_response["results"]
        if not search_results:
            raise RuntimeError(f"No search results returned for query: {query}")

        first_document_id = search_results[0]["documentId"]

        mcp_tools = checked(
            client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        ).json()
        tools_result = require_json_rpc_result(mcp_tools, "MCP tools/list")

        mcp_fetch = checked(
            client.post(
                "/mcp",
                headers=headers,
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "fetch_document",
                        "arguments": {"documentId": first_document_id}
                    }
                }
            )
        ).json()
        fetch_result = require_json_rpc_result(mcp_fetch, "MCP fetch_document")

        a2a_payload = update_a2a_question(load_a2a_payload(), query)
        a2a_response = checked(client.post("/a2a/v1", headers=headers, json=a2a_payload)).json()
        a2a_result = require_json_rpc_result(a2a_response, "A2A message/send")
        a2a_data = a2a_result["artifacts"][0]["parts"][0]["data"]

        draft_response = checked(
            client.post(
                "/reviews/drafts",
                headers=headers,
                json={
                    "topic": query,
                    "sourceDocumentIds": [result["documentId"] for result in search_results[:3]],
                    "outline": a2a_data["outline"],
                    "humanReviewRequired": True
                }
            )
        ).json()

        summary = {
            "agent": agent_card["name"],
            "agentEndpoint": agent_card["url"],
            "registryTrustLevel": registry_entry["trustLevel"],
            "traceId": DEFAULT_TRACE_ID,
            "query": query,
            "resultCount": len(search_results),
            "topDocument": first_document_id,
            "mcpTools": [tool["name"] for tool in tools_result["tools"]],
            "mcpFetchedTitle": fetch_result["content"][0]["json"]["title"],
            "a2aTaskState": a2a_result["status"]["state"],
            "a2aTraceId": a2a_result["metadata"]["traceId"],
            "draftId": draft_response["draftId"],
            "reviewUrl": draft_response["reviewUrl"]
        }

        if show_audit:
            audit_response = checked(client.get("/debug/audit-events", headers=headers, params={"limit": 20})).json()
            summary["auditEvents"] = audit_response["events"]

        if show_trace:
            trace_response = checked(client.get(f"/debug/traces/{DEFAULT_TRACE_ID}", headers=headers)).json()
            summary["trace"] = trace_response["events"]

        return summary


def print_summary(summary: dict[str, Any], json_only: bool) -> None:
    if json_only:
        print(json.dumps(summary, sort_keys=True))
        return

    trace = summary.pop("trace", None)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if trace:
        print("\nStack trace:")
        for event in trace:
            refs = ", ".join(event.get("artifactRefs", []))
            suffix = f" [{refs}]" if refs else ""
            print(
                f"- {event['layer']} / {event['component']}: "
                f"{event['event']} ({event['policyResult']}){suffix}"
            )


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    try:
        summary = run_workflow(base_url, args.query, args.show_audit, args.show_trace)
        print_summary(summary, args.json)
        return 0
    except httpx.ConnectError:
        print(
            f"Could not connect to {base_url}. Start the API first with: npm run api:dev",
            file=sys.stderr
        )
        return 1
    except httpx.HTTPStatusError as error:
        print(error.response.text, file=sys.stderr)
        return 1
    except (KeyError, IndexError, RuntimeError) as error:
        print(f"Demo workflow failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
