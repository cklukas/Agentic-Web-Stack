# Concepts

These pages explain the agent-specific technologies and architecture boundaries that are easy to confuse when first entering the Agentic Web ecosystem.

Each concept page includes a short use case and a small example message, metadata document, or tool definition.

## Core Concepts

- [Agent Card](./agent-card.md): machine-readable metadata that describes an agent, its capabilities, skills, endpoints, protocols, and authentication requirements.
- [Agent2Agent](./a2a.md): protocol layer for communication and collaboration between independent agents.
- [Model Context Protocol](./mcp.md): protocol layer for connecting an agent or AI application to tools, resources, and reusable prompts.
- [Agent Discovery](./agent-discovery.md): how clients find agents and evaluate discovery metadata.
- [Identity Delegation](./identity-delegation.md): scoped access when agents act for users, services, or organizations.
- [Trust Model](./trust-model.md): trust levels and evidence required before using an agent.
- [Agent Registry](./agent-registry.md): governed catalogs for approved agents and trust metadata.
- [Tool Use](./tool-use.md): deterministic operations exposed to agents through protocols or APIs.
- [Agent Memory](./memory.md): persistent and retrievable context beyond a single model call.
- [Evaluation](./evaluation.md): scenario checks for behavior, security, reliability, and observability.
- [Versioning and Governance](./versioning-governance.md): safe evolution of metadata, APIs, tools, and policies.

## Comparisons

- [MCP vs A2A](./mcp-vs-a2a.md): agent-to-tool and agent-to-agent boundaries.
- [Agent Card vs OpenAPI](./agent-card-vs-openapi.md): agent metadata and HTTP API contracts.
- [RAG vs Memory](./rag-vs-memory.md): retrieval pattern and persistent context layer.
- [Framework vs Protocol](./framework-vs-protocol.md): implementation productivity and interoperability boundaries.

## Related Reference Pages

- [Technology Origins](/references/technology-origins): historical context for when key technologies emerged, who developed them, and who stewards them.
- [Specifications](/specifications/): machine-readable examples linked from concept and topic pages.

## Quick Distinctions

| Concept | Main question | Typical artifact |
| --- | --- | --- |
| Agent Card | What agent is this, and what can it do? | JSON document at `/.well-known/agent-card.json` |
| A2A | How does one agent talk to another agent? | Agent Card, task messages, artifacts, streaming or push updates |
| MCP | How does an agent use external tools and context? | MCP server exposing tools, resources, and prompts |
| OpenAPI | How does software describe HTTP APIs? | `openapi.json` or `openapi.yaml` |
| OAuth2/OIDC | How does access and identity work? | Access tokens, ID tokens, scopes, claims, discovery metadata |
| Agent Registry | Which agents are approved for this environment? | Registry entry with domain, version, trust level, protocols, and policy |
