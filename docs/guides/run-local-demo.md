# Run the Local Demo

The local demo runs the **Literature Review Assistant** as a deterministic FastAPI service. It exposes the same contracts used throughout the documentation: Agent Card discovery, scoped JWT access, OpenAPI REST endpoints, MCP-style tools, A2A-style task delegation, and review draft creation.

No external model provider, identity provider, vector database, or graph database is required.

## Prerequisites

- Node.js 18 or newer
- npm
- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)

## Install

```bash
npm install
npm run api:sync
```

Check the local setup with:

```bash
npm run demo:doctor
```

The doctor checks Node.js, npm, uv, Python, required project files, and the default API port.

## Run the API

Start the FastAPI service:

```bash
npm run api:dev
```

The API listens on `http://127.0.0.1:8000`.

Useful endpoints:

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Service health check |
| `GET /.well-known/agent-card.json` | Localized Agent Card |
| `GET /registry/agents/{agentId}` | Local registry trust entry |
| `GET /openapi.json` | Localized OpenAPI contract |
| `GET /auth/dev-token` | Local scoped JWT helper |
| `POST /documents/search` | Search the deterministic corpus |
| `GET /documents/{documentId}` | Retrieve document metadata |
| `POST /reviews/drafts` | Create a human-reviewable draft |
| `POST /mcp` | MCP-shaped tools/list and tools/call endpoint |
| `POST /a2a/v1` | A2A-shaped message/send endpoint |
| `GET /debug/runtime` | Local runtime metadata, protected by `debug:read` |
| `GET /debug/audit-events` | Recent in-memory audit events, protected by `debug:read` |
| `GET /debug/traces/{traceId}` | Ordered architecture trace, protected by `debug:read` |

## Run the Workflow

In a second terminal, run:

```bash
npm run demo:run
```

The workflow:

1. Requests a local JWT with `research:read` and `drafts:write`.
2. Fetches the local Agent Card.
3. Checks the local registry trust entry.
4. Searches the document corpus through the REST API.
5. Lists and calls MCP tools.
6. Sends the A2A `message/send` request.
7. Creates a review draft that requires human review.
8. Prints a compact JSON summary.

The workflow runner also supports:

```bash
npm run demo:run -- --query "prompt injection access tokens" --show-audit
npm run demo:run -- --show-trace
npm run demo:run -- --base-url http://127.0.0.1:8000 --json
```

Use a different API origin with:

```bash
DEMO_API_URL=http://127.0.0.1:8000 npm run demo:run
```

## Validate

Run the one-command smoke test:

```bash
npm run demo:smoke
```

The smoke test starts the API on a free local port, waits for `/health`, runs the workflow, verifies the result, and shuts the server down.

Run the API tests:

```bash
npm run api:test
```

Run the full local check:

```bash
npm run check
```

`npm run check` validates specs, runs API tests, runs the smoke demo, and builds the documentation site.

## Trace IDs

Every request accepts `X-Trace-Id`. If the header is missing, the API creates one. The same value is returned in the `X-Trace-Id` response header and appears in audit events, JSON-RPC metadata, and A2A task metadata.

Example:

```bash
curl -H "X-Trace-Id: trace-manual-001" http://127.0.0.1:8000/health
```

## Debug Endpoints

Debug endpoints require the local `debug:read` scope.

```bash
TOKEN=$(curl -s "http://127.0.0.1:8000/auth/dev-token?scope=debug:read" | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/debug/runtime
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/debug/audit-events
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/debug/traces/trace-demo-001
```

These endpoints are for local inspection only. They do not expose raw tokens or secrets.

## Architecture Trace

Use `--show-trace` to see which stack layers were exercised:

```bash
npm run demo:run -- --show-trace
```

Example trace lines:

```text
- discovery / agent-card: agent_card_discovery (public) [spec:agent-card.json]
- discovery / agent-registry: agent_registry_lookup (approved) [spec:agent-registry.yaml]
- agent-protocols / mcp: mcp_tool_call (allowed)
- agent-protocols / a2a: a2a_message_send (allowed)
- applications / review-draft: review_draft_created (human_review_required)
```

## Troubleshooting

- Run `npm run demo:doctor` first when local setup fails.
- Use `npm run api:sync` after pulling dependency changes.
- If port `8000` is busy, `npm run demo:smoke` still works because it uses a free local port.
- If `npm run demo:run` cannot connect, start the API with `npm run api:dev`.

## Related Artifacts

- [End-to-End Demo](/guides/end-to-end-demo) explains the scenario.
- [Agent Card](/specs/demo/agent-card.json) is the discovery source.
- [Agent registry](/specs/demo/agent-registry.yaml) is the local trust source.
- [OpenAPI](/specs/demo/openapi.yaml) is the REST contract.
- [MCP tools](/specs/demo/mcp-tools.json) define the tool surface.
- [A2A message](/specs/demo/a2a-message-send.json) is the delegated task request.
- [Evaluation scenarios](/specs/demo/evaluation-scenarios.yaml) drive behavior tests.
