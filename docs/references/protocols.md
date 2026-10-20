# Protocols

## Model Context Protocol

- [MCP specification](https://modelcontextprotocol.io/specification) - authoritative protocol specification for MCP.
- [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro) - official overview and getting started material.
- [MCP GitHub organization](https://github.com/modelcontextprotocol) - reference repositories and SDKs.

MCP is tracked in this project as the primary agent-to-tool and agent-to-resource protocol.

## Agent2Agent Protocol

- [A2A Protocol](https://a2a-protocol.org/latest/) - official A2A documentation home.
- [A2A Specification](https://a2a-protocol.org/latest/specification/) - current protocol specification.
- [A2A Agent Discovery](https://a2a-protocol.org/latest/topics/agent-discovery/) - Agent Card discovery strategies, security notes, and caching guidance.
- [A2A and MCP](https://a2a-protocol.org/latest/topics/a2a-and-mcp/) - official explanation of how A2A and MCP complement each other.
- [A2A GitHub repository](https://github.com/a2aproject/A2A) - protocol repository and specification material.
- [Google A2A announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) - original public announcement and motivation.

A2A is tracked in this project as the primary agent-to-agent discovery, capability exchange, and task delegation protocol.

## Related Web Protocols

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - Machine-readable API contract format commonly consumed by tools, gateways, and agents.
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) - Identity protocol layered on OAuth2 for authentication and ID tokens.
- [OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749) - Authorization framework for delegated, scoped access to protected resources.

## Related Documentation Discovery

[llms.txt](https://llmstxt.org/) is a community proposal for a Markdown documentation index, rather than an agent messaging or tool protocol. It can help clients locate context before using MCP, A2A, or an API. The [local concept](/concepts/llms-txt) and [discovery reference](./standards.md#emerging-community-proposals) explain its separate role.
