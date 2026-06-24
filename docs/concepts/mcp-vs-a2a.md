# MCP vs A2A

MCP and A2A solve different interoperability problems.

| Question | MCP | A2A |
| --- | --- | --- |
| Main relationship | Agent or AI app to tools and resources | Agent to agent |
| Typical remote thing | Tool server, API adapter, file system, data source | Autonomous agent with its own task lifecycle |
| Core operation | List and call tools, read resources, use prompts | Send messages, create tasks, exchange artifacts |
| Best fit | Controlled tool access | Delegated work across agent boundaries |
| Demo artifact | [mcp-tools.json](/specs/demo/mcp-tools.json) | [a2a-message-send.json](/specs/demo/a2a-message-send.json) |

## Decision Rule

Use MCP when the remote capability is a callable tool or context provider. Use A2A when the remote capability is another agent that accepts delegated work and returns task state or artifacts.

## Related Pages

- [Model Context Protocol](./mcp.md)
- [Agent2Agent](./a2a.md)
- [Tool Use](./tool-use.md)
