# Model Context Protocol

Model Context Protocol, usually shortened to MCP, is an open protocol for connecting AI applications and agents to external systems. An MCP server exposes capabilities such as tools, resources, and prompts. An MCP client inside an AI application discovers and invokes those capabilities.

MCP is best understood as the agent-to-tool layer of the stack.

## Origin and Stewardship

MCP was introduced by Anthropic in November 2024 as an open standard for connecting AI applications to external tools and data sources. Its initial framing was a response to integration fragmentation: every AI application needed access to files, repositories, databases, SaaS APIs, and internal systems, but each integration tended to be custom.

The protocol uses a host-client-server architecture. A user-facing AI application acts as the host, the host runs one or more MCP clients, and those clients connect to MCP servers that expose tools, resources, and prompts.

For architecture work, MCP should be treated as an agent integration protocol, not an agent collaboration protocol. MCP is strongest when the remote thing is a tool, API, data source, file system, or reusable prompt. A2A is the better fit when the remote thing is another autonomous agent with its own task lifecycle.

## What MCP Solves

MCP avoids building one-off integrations for every AI application and every data source. Instead of each agent inventing a custom plugin system, MCP defines a common protocol for exposing external context and actions.

## Core Building Blocks

| Building block | Role |
| --- | --- |
| Host | AI application that the user interacts with, such as an IDE, chat app, or agent runtime |
| Client | Protocol client inside the host that connects to MCP servers |
| Server | Process or service that exposes tools, resources, and prompts |
| Tool | Callable operation, such as querying a database or calling an API |
| Resource | Context object identified by a URI, such as a file, schema, record, or document |
| Prompt | Reusable prompt template or structured interaction pattern |

## Tools, Resources, and Prompts

- Tools are model-controlled callable actions. They are useful for APIs, database queries, calculations, repository operations, and other side-effect-aware functions.
- Resources are application-controlled context. They are useful for files, database schemas, knowledge documents, and other data the host may include in model context.
- Prompts are user-controlled templates. They are useful for reusable workflows such as code review, summarization, analysis, or structured task setup.

## Common Technology Stack

- MCP SDKs: TypeScript, Python, Java, Kotlin, C#, or framework-specific integrations.
- Server transport: stdio for local tools, HTTP or streaming HTTP for remote services.
- Tool backends: REST APIs, databases, search services, file systems, SaaS APIs.
- Identity: OAuth2 or gateway-authenticated remote MCP services where sensitive data is involved.
- Security controls: user consent, tool allowlists, input validation, output filtering, and audit logs.

## MCP vs A2A

| Question | Use MCP | Use A2A |
| --- | --- | --- |
| Is the remote thing a tool, API, database, or resource? | Yes | Usually no |
| Is the remote thing another autonomous agent? | Usually no | Yes |
| Do you need capability discovery for tools and prompts? | Yes | No |
| Do you need task delegation to another agent? | No | Yes |

## Example Use Case

A research agent needs access to a private document index. Instead of giving the model direct database credentials, the application connects to an MCP server that exposes a controlled `search_documents` tool.

## Example MCP Tool

Clients discover tools with `tools/list` and invoke them with `tools/call`.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

Example response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "search_documents",
        "title": "Search Documents",
        "description": "Searches approved internal documents and returns matching passages with source IDs.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "Natural language search query"
            },
            "limit": {
              "type": "integer",
              "minimum": 1,
              "maximum": 10,
              "default": 5
            }
          },
          "required": ["query"]
        },
        "outputSchema": {
          "type": "object",
          "properties": {
            "results": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "sourceId": { "type": "string" },
                  "title": { "type": "string" },
                  "snippet": { "type": "string" }
                },
                "required": ["sourceId", "snippet"]
              }
            }
          },
          "required": ["results"]
        }
      }
    ]
  }
}
```

Example artifact: [mcp-tools.json](/specs/demo/mcp-tools.json).

## References and Further Reading

- [Introducing Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) - Anthropic's November 2024 launch post explaining the motivation for MCP and the integration problem it targets.
- [MCP Introduction](https://modelcontextprotocol.io/docs/getting-started/intro) - Official introductory documentation for MCP concepts, architecture, and use cases.
- [MCP Specification](https://modelcontextprotocol.io/specification) - Normative protocol reference for clients, servers, lifecycle behavior, capabilities, and transports.
- [MCP Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) - Official server feature page for model-controlled callable operations.
- [MCP Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources) - Official server feature page for URI-addressed context exposed by MCP servers.
- [MCP Prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts) - Official server feature page for reusable prompt templates and structured workflows.
- [Agent Protocols Topic](/topics/agent-protocols) - Topic guide comparing MCP, A2A, Agent Cards, and protocol architecture.
