# Agent Protocols

## Topic Summary

The agent protocol layer defines how agents expose tools and resources, exchange capabilities, delegate tasks, and collaborate with other agents.

## Stack Level

Agent protocols are Layer 4 of the Agentic Web Stack. This layer sits above ordinary APIs and gives agents a shared way to discover tools, expose context, publish capabilities, delegate work, stream progress, and exchange task artifacts.

## Goals

- Document Model Context Protocol as the agent-to-tool integration layer.
- Document Agent2Agent as the agent-to-agent collaboration layer.
- Keep protocol experiments modular so alternatives can be compared.

## Common Tech Stack

| Technology | Role in agent protocols |
| --- | --- |
| MCP | Agent-to-tool and agent-to-resource protocol for tools, resources, and prompts |
| A2A | Agent-to-agent protocol for discovery, tasks, messages, artifacts, and collaboration |
| Agent Card | A2A discovery metadata for remote agent identity, skills, protocols, and auth |
| JSON-RPC | Common request and response style used by protocol implementations |
| Streaming HTTP or SSE | Progress updates and long-running task output |
| Webhooks or push notifications | Asynchronous completion and update delivery |
| Protocol SDKs | Python, TypeScript, Java, Go, C#, or Rust libraries for implementing clients and servers |

## Reference Scenario

The Literature Review Assistant accepts delegated work through A2A and uses MCP internally for controlled access to document tools. This keeps remote agent collaboration separate from tool and resource access.

## Related Materials

- [Agent2Agent concept](/concepts/a2a)
- [Model Context Protocol concept](/concepts/mcp)
- [Protocol Selection Decision](/decisions/protocol-selection)

## Standards and Protocols

- Model Context Protocol
- Agent2Agent Protocol
- JSON-RPC style tool calls where required by protocol implementations
- Capability exchange and task lifecycle metadata

## Example Use Case

A research coordinator agent accepts a user task through A2A, then uses MCP tools internally to search documents, fetch metadata, and create a bibliography. The client sees one remote agent, while the coordinator agent composes lower-level tools behind its own boundary.

## Example Protocol Specification Sketch

```yaml
remoteAgent:
  name: Research Coordinator Agent
  discovery:
    agentCard: https://research.example.edu/.well-known/agent-card.json
  a2a:
    endpoint: https://research.example.edu/a2a/v1
    supportedOperations:
      - message/send
      - message/stream
      - tasks/get
    outputModes:
      - text/plain
      - application/json
internalTools:
  mcpServers:
    - name: document-search
      transport: streamable-http
      url: https://tools.example.edu/mcp/documents
      tools:
        - search_documents
        - fetch_document
    - name: citation-tools
      transport: stdio
      tools:
        - format_citation
workflow:
  - receiveTaskViaA2A
  - searchDocumentsViaMCP
  - fetchRelevantSourcesViaMCP
  - returnSummaryAndArtifactsViaA2A
```

Example artifacts: [a2a-message-send.json](/specs/demo/a2a-message-send.json) and [mcp-tools.json](/specs/demo/mcp-tools.json).

## Reference Links and Papers

- [Technology Origins](/references/technology-origins) - Local reference page with first public milestones, origin organizations, governance notes, and curated source links.
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification) - Normative MCP reference for client-server behavior, capabilities, lifecycle, and transport details.
- [Model Context Protocol documentation](https://modelcontextprotocol.io/docs/getting-started/intro) - Official introduction to MCP concepts, architecture, and implementation paths.
- [MCP tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) - Official description of callable operations exposed by MCP servers.
- [MCP resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources) - Official description of URI-addressed context objects exposed by MCP servers.
- [MCP prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts) - Official description of reusable prompt templates exposed by MCP servers.
- [A2A Protocol](https://a2a-protocol.org/latest/) - Official A2A documentation home for agent-to-agent interoperability.
- [A2A Specification](https://a2a-protocol.org/latest/specification/) - Normative A2A protocol reference for Agent Cards, skills, tasks, messages, artifacts, and events.
- [A2A and MCP](https://a2a-protocol.org/latest/topics/a2a-and-mcp/) - Official comparison that explains why A2A and MCP are complementary.
- [Agent2Agent Protocol repository](https://github.com/a2aproject/A2A) - Source repository for protocol materials, examples, issues, and community development.
- [Google announcement: Agent2Agent Protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) - Original Google launch post describing the interoperability need behind A2A.
- [Agent Card concept](/concepts/agent-card) - Local concept page for the A2A discovery metadata document.

## Design Considerations

- Use A2A when a remote service owns task state and returns artifacts over time.
- Use MCP when an agent needs a controlled interface to tools, resources, or prompts.
- Keep deterministic APIs documented separately from protocol wrappers.
- Document security assumptions before exposing external tools or remote agents.
