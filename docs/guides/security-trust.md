# Security and Trust

Agentic systems extend ordinary web security with new trust boundaries: model context, tool execution, delegated identity, remote agent discovery, and cross-agent task state.

This page defines security expectations for the Literature Review Assistant scenario and other agent-native systems.

## Trust Boundaries

| Boundary | Risk | Required control |
| --- | --- | --- |
| Public discovery metadata | Malicious or stale Agent Cards | HTTPS, cache validation, allowlisted registries for sensitive deployments |
| Identity provider to service | Token misuse or wrong audience | OIDC discovery, audience checks, expiry checks, scope checks |
| Agent to API | Excessive permissions | Least-privilege OAuth2 scopes and policy enforcement |
| Agent to MCP tool | Tool abuse or unsafe side effects | Tool allowlists, input validation, user approval for writes |
| Retrieval to model context | Prompt injection in documents | Treat retrieved text as untrusted data and isolate instructions |
| Model output to action | Hallucinated commands or unsafe drafts | Human approval gates and deterministic API validation |
| Multi-tenant data | Data leakage across users or organizations | Tenant claims, row-level filtering, audit logs |

## Threats to Cover

- **Malicious Agent Card:** a card advertises a fake endpoint or overbroad skills.
- **Delegation confusion:** an agent acts with service privileges instead of the signed-in user's scopes.
- **Prompt injection:** retrieved content instructs the model to ignore policy or reveal secrets.
- **Tool abuse:** a tool call performs a side effect outside the user's intent.
- **Token leakage:** access tokens are logged, embedded in prompts, or returned in artifacts.
- **SSRF-style tool risk:** URL-fetching tools access internal metadata or private network targets.
- **Stale metadata:** clients trust an old Agent Card after protocols or auth requirements changed.
- **Tenant isolation failure:** memory retrieval returns another tenant's source material.

## Security Checklist

- Validate Agent Cards against an expected domain, transport, and security policy before invoking an agent.
- Require HTTPS for public discovery, API calls, A2A endpoints, and remote MCP servers.
- Validate token issuer, audience, expiry, signature, scopes, tenant, and authorized party.
- Never place access tokens, refresh tokens, API keys, or secrets into model context.
- Treat retrieved documents, web pages, email, and remote agent output as untrusted content.
- Require human approval before creating, sending, publishing, deleting, or externally sharing content.
- Restrict MCP tools with allowlists, schema validation, timeouts, rate limits, and audit logs.
- Block internal network targets unless a tool is explicitly designed for internal access.
- Store trace IDs, tool calls, policy decisions, and approval events without storing raw secrets.
- Define retention and deletion policy before storing embeddings, prompts, outputs, or task artifacts.

## Example Artifacts

- [OIDC client configuration](/specs/demo/oidc-client.example.json)
- [OpenAPI security schemes](/specs/demo/openapi.yaml)
- [A2A message example](/specs/demo/a2a-message-send.json)
- [MCP tool list](/specs/demo/mcp-tools.json)
- [Evaluation scenarios](/specs/demo/evaluation-scenarios.yaml)

## Related Topics

- [Identity](/topics/identity)
- [Discovery](/topics/discovery)
- [Agent Protocols](/topics/agent-protocols)
- [Operations and Evaluation](/guides/operations-evaluation)
