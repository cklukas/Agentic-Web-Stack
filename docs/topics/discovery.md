# Discovery

## Topic Summary

The discovery layer lets agents find services, identify capabilities, and locate machine-readable metadata before attempting integration.

## Stack Level

Discovery is Layer 1 of the Agentic Web Stack. It is the first machine-readable handshake between a domain and an agent client: what exists here, which metadata is public, which endpoints are available, and where deeper API or agent descriptions can be fetched.

## Goals

- Define predictable discovery endpoints for agent-native services.
- Document how existing web discovery mechanisms apply to agents.
- Show how Agent Cards, OpenAPI, robots.txt, sitemaps, llms.txt, and registries fit together.

## Common Tech Stack

| Technology | Role in discovery |
| --- | --- |
| Agent Card | A2A-compatible JSON metadata for agent identity, skills, endpoints, protocols, and authentication requirements |
| Agent registry | Governed catalog entry for approved domain, current Agent Card version, trust level, allowed protocols, scopes, and review status |
| `/.well-known/agent-card.json` | Standard well-known location for public A2A Agent Card discovery |
| `/.well-known/` URIs | General pattern for predictable site metadata |
| OpenAPI | Machine-readable HTTP API discovery through `openapi.json` or `openapi.yaml` |
| robots.txt | Crawler and agent access hints for web paths |
| sitemap.xml | URL inventory for documentation, pages, and crawlable resources |
| llms.txt (proposal) | Curated Markdown entry point to documentation for agent context |
| Registries or catalogs | Enterprise or marketplace-style lookup of approved Agent Cards and services |

## Reference Scenario

The Literature Review Assistant publishes a public Agent Card and has a local registry entry. A client can inspect public capabilities first, check registry trust metadata when governance requires it, then authenticate when richer or user-specific metadata is required.

## Related Materials

- [Agent Card concept](/concepts/agent-card)
- [Agent Discovery concept](/concepts/agent-discovery)
- [llms.txt concept](/concepts/llms-txt)
- [Agent Registry concept](/concepts/agent-registry)
- [End-to-End Demo](/guides/end-to-end-demo)
- [Specifications](/specifications/)

## Standards and Protocols

- Well-Known URIs
- robots.txt
- sitemap.xml
- llms.txt (community proposal)
- OpenAPI descriptions
- Agent Cards and A2A discovery metadata

## Example Use Case

A documentation site exposes a public research agent and a small API. A visiting client agent should be able to discover the Agent Card, inspect the OpenAPI description, respect crawler hints, and find human-readable documentation without asking a developer for out-of-band configuration.

## Example Specification Sketch

For documentation discovery, the client could also consult an [llms.txt index](/concepts/llms-txt) to locate relevant guides before using the API. The following sketch illustrates a possible deployment rather than the local demo's current endpoints.

```yaml
domain: research.example.edu
publicDiscovery:
  agentCard:
    url: https://research.example.edu/.well-known/agent-card.json
    contentType: application/json
    cacheControl: public, max-age=300
  openapi:
    url: https://research.example.edu/openapi.json
    contentType: application/vnd.oai.openapi+json
  robots:
    url: https://research.example.edu/robots.txt
    policy:
      userAgent: "*"
      allow:
        - /docs/
        - /.well-known/agent-card.json
      disallow:
        - /admin/
        - /internal/
  sitemap:
    url: https://research.example.edu/sitemap.xml
  documentationIndex:
    url: https://research.example.edu/docs/llms.txt
    status: optional-community-proposal
privateDiscovery:
  extendedAgentCard:
    url: https://research.example.edu/a2a/v1/extendedAgentCard
    auth: oidc
```

Example artifact: [agent-card.json](/specs/demo/agent-card.json).

## Reference Links and Papers

- [Technology Origins](/references/technology-origins) - Local reference page for when discovery-related technologies emerged and who stewards them.
- [RFC 8615: Well-Known Uniform Resource Identifiers](https://www.rfc-editor.org/rfc/rfc8615) - IETF standard for predictable `/.well-known/` metadata locations.
- [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309) - IETF standard for `robots.txt` crawler access rules.
- [Sitemaps XML format](https://www.sitemaps.org/protocol.html) - Conventional XML format for listing crawlable URLs.
- [llms.txt proposal](https://llmstxt.org/) - Community proposal for an agent-readable documentation index.
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - Machine-readable HTTP API contract used by tools, gateways, SDK generators, and agents.
- [A2A Agent Discovery](https://a2a-protocol.org/latest/topics/agent-discovery/) - Official A2A guide for Agent Cards, discovery paths, registries, security, and caching.
- [Agent2Agent Protocol repository](https://github.com/a2aproject/A2A) - Source repository for A2A protocol materials and examples.
- [Agent Card concept](/concepts/agent-card) - Local concept page focused on the agent discovery metadata document.

## Design Considerations

- Publish `/.well-known/agent-card.json` at a stable HTTPS origin.
- Expose `/openapi.json` or `/openapi.yaml` for deterministic APIs.
- Consider `llms.txt` for documentation context; keep its links current and treat fetched content as external data under the client's trust policy.
- Keep `robots.txt` and `sitemap.xml` aligned with what agents are allowed to crawl.
- Use cache headers and version fields so clients can detect stale metadata.
