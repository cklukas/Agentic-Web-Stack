# Decisions

Decision guides explain practical starting points and the tradeoffs behind them.

Use these pages when choosing technologies for an agent-native system:

- [Protocol Selection](./protocol-selection.md)
- [API Style](./api-style.md)
- [Memory Store Selection](./memory-store-selection.md)
- [Model Deployment](./model-deployment.md)
- [Agent Framework Selection](./agent-framework-selection.md)

## Recommended Starting Points

| Area | Starting point |
| --- | --- |
| Protocols | A2A for agent-to-agent work, MCP for agent-to-tool work, OpenAPI for deterministic APIs |
| API style | REST with OpenAPI first; GraphQL only when query flexibility is needed |
| Memory | Qdrant-style vector index plus Neo4j-style graph model for the demo architecture |
| Models | Model gateway abstraction with hosted primary routes and local private classification route |
| Agent framework | Start with explicit orchestration; evaluate LangGraph for stateful long-running workflows |
