# Agent Card

An Agent Card is a machine-readable JSON document that describes an agent to clients and other agents. It is the agent-native equivalent of a service profile: identity, capabilities, skills, endpoints, supported interfaces, and security requirements in one discoverable place.

In the A2A ecosystem, the current well-known discovery location is:

```text
https://example.com/.well-known/agent-card.json
```

## Origin and Stewardship

The Agent Card emerged with the A2A protocol work introduced by Google in 2025 and later donated to the Linux Foundation. It is not a separate product or vendor-specific registry format. It is the A2A discovery document that lets clients inspect a remote agent before starting a task.

The design borrows from a familiar web pattern: publish machine-readable metadata at a predictable `.well-known` URL. The general `.well-known` URI mechanism is standardized by RFC 8615. A2A applies that pattern to agent discovery with the current path `/.well-known/agent-card.json`.

This provenance matters because an Agent Card sits between the traditional web and the agent-native web. It uses ordinary HTTPS and JSON, but describes agent-specific concepts such as skills, streaming support, push notifications, task capabilities, and authentication requirements.

## Why Agent Cards Matter

Without an Agent Card, another agent needs out-of-band knowledge to know whether a remote agent is useful, safe to call, or compatible with the client. With an Agent Card, a client can inspect the remote agent before starting a task.

Agent Cards support:

- capability discovery
- endpoint discovery
- protocol negotiation
- authentication planning
- skill selection
- user and developer documentation links
- public and authenticated extended metadata

## Common Fields

The exact schema is defined by the A2A specification, but the important categories are:

| Category | Purpose |
| --- | --- |
| Identity | Agent name, description, provider, version, and documentation URL |
| Endpoint | URL or interface information for reaching the agent service |
| Capabilities | Features such as streaming, push notifications, or state transition history |
| Skills | Task-oriented descriptions with IDs, names, input modes, output modes, and examples |
| Security | Authentication schemes such as bearer tokens, OAuth2, OpenID Connect, API keys, or mTLS |
| Extensions | Optional protocol features or vendor-specific additions |

## Public vs Extended Agent Cards

A public Agent Card should contain enough information for discovery without exposing secrets, internal URLs, privileged skills, or sensitive operational details.

An extended Agent Card can provide richer metadata after the client authenticates. This is useful for enterprise agents where capabilities differ by tenant, user role, or policy.

## Discovery Strategies

- Well-known URI: publish the card at `/.well-known/agent-card.json`.
- Registry or catalog: publish cards to a curated internal or public catalog.
- Direct configuration: configure trusted clients with card URLs or card content.

## Security Notes

- Do not embed static secrets in Agent Cards.
- Use HTTPS for integrity and server authenticity.
- Protect sensitive or internal cards with authentication and authorization.
- Consider signed cards where clients need tamper evidence.
- Apply normal HTTP caching with `Cache-Control` and `ETag` where appropriate.

## Example Use Case

A university library exposes a research assistant agent. A client agent discovers the public Agent Card, sees that the service can search scholarly sources and summarize papers, then authenticates to retrieve an extended card with institution-specific collections.

## Example Agent Card

This is an illustrative public card for `https://research.example.edu/.well-known/agent-card.json`. Validate field names and security scheme details against the current A2A specification before using a card in production.

```json
{
  "name": "Literature Research Agent",
  "description": "Finds papers, retrieves abstracts, and creates short research summaries with citations.",
  "supportedInterfaces": [
    {
      "url": "https://research.example.edu/a2a/v1",
      "protocolBinding": "HTTP+JSON",
      "protocolVersion": "1.0"
    }
  ],
  "provider": {
    "organization": "Example University Library",
    "url": "https://research.example.edu"
  },
  "version": "0.1.0",
  "documentationUrl": "https://research.example.edu/docs/agents/literature-research",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "extendedAgentCard": true
  },
  "securitySchemes": {
    "campusOidc": {
      "openIdConnectSecurityScheme": {
        "openIdConnectUrl": "https://auth.example.edu/.well-known/openid-configuration"
      }
    }
  },
  "security": [
    {
      "campusOidc": ["openid", "profile", "research:read"]
    }
  ],
  "defaultInputModes": ["text/plain", "application/json"],
  "defaultOutputModes": ["text/plain", "application/json"],
  "skills": [
    {
      "id": "paper-search",
      "name": "Paper Search",
      "description": "Searches library indexes and open scholarly sources for papers matching a research question.",
      "tags": ["research", "search", "papers", "citations"],
      "examples": [
        "Find recent papers about agent-to-agent interoperability.",
        "{\"query\":\"retrieval augmented generation evaluation\",\"yearFrom\":2023}"
      ],
      "inputModes": ["text/plain", "application/json"],
      "outputModes": ["application/json", "text/plain"]
    },
    {
      "id": "literature-summary",
      "name": "Literature Summary",
      "description": "Summarizes selected papers and returns key claims, methods, limitations, and citation metadata.",
      "tags": ["summarization", "literature-review", "citations"],
      "examples": [
        "Summarize these five papers and compare their evaluation methods."
      ],
      "inputModes": ["application/json"],
      "outputModes": ["text/plain", "application/json"]
    }
  ]
}
```

Example artifact: [agent-card.json](/specs/demo/agent-card.json).

## References and Further Reading

- [A2A Agent Discovery](https://a2a-protocol.org/latest/topics/agent-discovery/) - Official A2A guide to Agent Cards, discovery mechanisms, sensitive metadata, security considerations, and caching.
- [A2A Specification](https://a2a-protocol.org/latest/specification/) - Normative schema reference for Agent Card fields, capabilities, skills, provider metadata, and security schemes.
- [RFC 8615: Well-Known URIs](https://www.rfc-editor.org/rfc/rfc8615) - IETF standard defining the `.well-known` URI pattern used by many discovery mechanisms.
- [A2A Protocol](https://a2a-protocol.org/latest/) - Broader protocol context for why Agent Cards exist and how they are used by A2A clients.
- [Google Cloud donates A2A to the Linux Foundation](https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/) - Historical and governance context for A2A and the Agent Card model.
- [Agent Protocols Topic](/topics/agent-protocols) - Local topic guide for the protocol layer where Agent Cards belong.
- [Discovery Topic](/topics/discovery) - Local topic guide for Agent Cards, OpenAPI, robots.txt, sitemap.xml, and registry-based discovery.
