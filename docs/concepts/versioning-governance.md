# Versioning and Governance

Versioning and governance answer: "How can clients safely keep using an agent system while metadata, schemas, tools, policies, and protocols evolve?"

Agentic systems have multiple contracts. A production change may touch an Agent Card, OpenAPI contract, MCP tool schema, A2A behavior, memory configuration, model route, policy rule, or evaluation suite.

## Governance Rules

- Version machine-readable metadata that clients depend on.
- Preserve operation IDs and tool names unless intentionally versioned.
- Treat Agent Card changes as discovery changes, not just documentation edits.
- Reject stale metadata when the version affects safety or compatibility.
- Keep evaluation scenarios aligned with protocol and policy changes.
- Record governance decisions in registry metadata or a policy system.

## Demo Mapping

The demo rejects stale A2A requests when the supplied Agent Card version does not match the expected version. Registry metadata records the currently approved Agent Card version.

## Related Pages

- [Agent Registry](./agent-registry.md)
- [Agent Discovery](./agent-discovery.md)
- [Operations and Evaluation](/guides/operations-evaluation)
