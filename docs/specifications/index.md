# Specifications

This section collects machine-readable examples for the Literature Review Assistant reference scenario.

These files are non-normative demo artifacts unless a linked standard says otherwise. They are checked to keep the examples parseable, linked, and internally consistent.

The local runnable demo uses these artifacts as its contract source and patches only local URLs at runtime.

## Demo Artifacts

| Artifact | Purpose | Used by |
| --- | --- | --- |
| [agent-card.json](/specs/demo/agent-card.json) | Public Agent Card for the Literature Review Assistant | [Discovery](/topics/discovery), [Agent Card](/concepts/agent-card) |
| [agent-registry.yaml](/specs/demo/agent-registry.yaml) | Non-normative registry entry with approved domain, current Agent Card version, trust level, allowed protocols, scopes, and review metadata | [Agent Registry](/concepts/agent-registry), [Trust Model](/concepts/trust-model) |
| [openapi.yaml](/specs/demo/openapi.yaml) | OpenAPI 3.1 contract for registry lookup, document search, review drafts, and local trace inspection | [APIs](/topics/apis) |
| [oidc-client.example.json](/specs/demo/oidc-client.example.json) | OIDC/OAuth2 client and scope model | [Identity](/topics/identity) |
| [mcp-tools.json](/specs/demo/mcp-tools.json) | MCP tools/list example for document tools | [MCP](/concepts/mcp), [Agent Protocols](/topics/agent-protocols) |
| [a2a-message-send.json](/specs/demo/a2a-message-send.json) | A2A message/send example request | [A2A](/concepts/a2a), [Agent Protocols](/topics/agent-protocols) |
| [memory.yaml](/specs/demo/memory.yaml) | Vector and graph memory configuration | [Memory](/topics/memory) |
| [model-routing.yaml](/specs/demo/model-routing.yaml) | Model gateway routing policy | [Models](/topics/models) |
| [application-workflow.yaml](/specs/demo/application-workflow.yaml) | End-to-end application workflow | [Applications](/topics/applications), [End-to-End Demo](/guides/end-to-end-demo) |
| [evaluation-scenarios.yaml](/specs/demo/evaluation-scenarios.yaml) | Evaluation scenarios for agent behavior, auth failures, tool failures, and stale discovery metadata | [Operations and Evaluation](/guides/operations-evaluation) |

## Artifact-to-Layer Map

| Stack layer | Artifact evidence | Why it exists |
| --- | --- | --- |
| Discovery | [agent-card.json](/specs/demo/agent-card.json), [agent-registry.yaml](/specs/demo/agent-registry.yaml) | Publish self-description and local trust approval |
| Identity | [oidc-client.example.json](/specs/demo/oidc-client.example.json) | Model delegated scopes, claims, audience, and token handling |
| APIs | [openapi.yaml](/specs/demo/openapi.yaml) | Define deterministic registry, document, draft, and trace operations |
| Agent Protocols | [mcp-tools.json](/specs/demo/mcp-tools.json), [a2a-message-send.json](/specs/demo/a2a-message-send.json) | Show tool access and delegated agent work |
| Memory | [memory.yaml](/specs/demo/memory.yaml) | Model vector retrieval, graph expansion, and visibility filters |
| Models | [model-routing.yaml](/specs/demo/model-routing.yaml) | Describe provider-neutral routing and usage capture |
| Applications | [application-workflow.yaml](/specs/demo/application-workflow.yaml), [evaluation-scenarios.yaml](/specs/demo/evaluation-scenarios.yaml) | Compose the workflow and verify expected behavior |

## Runnable Demo

[Run the Local Demo](/guides/run-local-demo) shows how the FastAPI service exposes the Agent Card, registry entry, OpenAPI contract, MCP tools, A2A endpoint, scoped dev tokens, document search, trace output, and review draft creation from the same reference scenario.

## Validation

The published examples are checked for:

- required demo files exist
- JSON and YAML files parse
- demo files validate against local schemas in `specs/schemas/`
- MCP nested input and output schemas compile
- `openapi.yaml` passes Redocly lint
- docs links to `/specs/demo/...` point at real files

## Schema Scope

Local schemas in `specs/schemas/` validate the reference examples. They are intentionally not full A2A, MCP, OAuth2, OpenID Connect, OpenAPI, or model-provider conformance schemas.
