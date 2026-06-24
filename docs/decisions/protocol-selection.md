# Protocol Selection

## Recommended Starting Point

Use **A2A** when the remote system is another autonomous agent. Use **MCP** when the remote system is a tool, resource, prompt, database, or API adapter. Use **direct OpenAPI calls** for deterministic service operations that do not need an agent protocol.

## Tradeoffs

| Choice | Best fit | Strength | Cost |
| --- | --- | --- | --- |
| Direct API call | Deterministic service operation | Simple, debuggable, mature web tooling | No agent-native task lifecycle |
| MCP | Agent-to-tool/resource integration | Tool discovery, schemas, reusable servers | Does not represent another autonomous agent |
| A2A | Agent-to-agent collaboration | Agent Card discovery, task state, artifacts, delegation | Newer ecosystem and evolving implementations |
| Workflow framework | Local orchestration inside one app | Control over state and human-in-the-loop flow | Not an interoperability protocol |

## Architecture Guidance

- Keep OpenAPI as the contract for deterministic backend operations.
- Wrap APIs with MCP only when agent hosts need discoverable tools.
- Publish A2A only for services that behave like remote agents with task ownership.
- Do not use A2A to hide ordinary CRUD APIs.
- Do not use MCP to represent another organization-owned autonomous agent.

## Example Artifacts

- [a2a-message-send.json](/specs/demo/a2a-message-send.json)
- [mcp-tools.json](/specs/demo/mcp-tools.json)
- [openapi.yaml](/specs/demo/openapi.yaml)
