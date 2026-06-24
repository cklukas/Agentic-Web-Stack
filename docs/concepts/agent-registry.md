# Agent Registry

An agent registry is a catalog of approved or known agents. It complements public discovery by adding local governance metadata.

Agent Cards answer what an agent says about itself. Registries answer whether a client should trust and use that agent in a specific organization or environment.

## Registry Responsibilities

- Map an agent ID to approved domains and endpoints.
- Record the current approved Agent Card version.
- List allowed protocols and required scopes.
- Record trust level, review status, and ownership.
- Provide policy metadata such as human-review and trace requirements.

## Demo Artifact

The demo registry is [agent-registry.yaml](/specs/demo/agent-registry.yaml). It is non-normative and intentionally small:

```yaml
agents:
  - id: literature-review-assistant
    trustLevel: organization-approved
    allowedProtocols: [openapi, mcp, a2a]
    requiredScopes: [research:read, drafts:write]
```

The local API exposes this entry at:

```text
GET /registry/agents/literature-review-assistant
```

## Related Pages

- [Agent Discovery](./agent-discovery.md)
- [Trust Model](./trust-model.md)
- [Specifications](/specifications/)
