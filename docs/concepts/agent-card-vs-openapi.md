# Agent Card vs OpenAPI

Agent Cards and OpenAPI describe different surfaces.

| Question | Agent Card | OpenAPI |
| --- | --- | --- |
| Describes | An agent identity and capabilities | HTTP API operations and schemas |
| Main user | Agent clients and registries | Developers, agents, gateways, SDKs |
| Typical location | `/.well-known/agent-card.json` | `/openapi.json` or `/openapi.yaml` |
| Contains | Skills, endpoints, auth, protocols, modes | Paths, methods, parameters, request/response schemas |
| Demo artifact | [agent-card.json](/specs/demo/agent-card.json) | [openapi.yaml](/specs/demo/openapi.yaml) |

## Decision Rule

Use an Agent Card to decide whether an agent is the right counterpart. Use OpenAPI to call deterministic HTTP operations once the client knows which service capability it needs.

## Related Pages

- [Agent Card](./agent-card.md)
- [Agent Discovery](./agent-discovery.md)
- [APIs topic](/topics/apis)
