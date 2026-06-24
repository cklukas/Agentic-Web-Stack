# Topic Guides

Topic guides explain the Agentic Web Stack by responsibility area. Read them when you want practical context, example use cases, and representative metadata, API, protocol, or workflow sketches.

## Web Foundations

These topics cover the substrate that agent systems inherit from the web and API ecosystem.

- [Discovery](./discovery.md) - Agent Cards, well-known URLs, OpenAPI descriptions, crawler hints, sitemaps, and registries.
- [Identity](./identity.md) - OAuth2, OpenID Connect, JWTs, scopes, claims, delegated access, and policy enforcement.
- [APIs](./apis.md) - REST, GraphQL, OpenAPI, JSON Schema, service contracts, and deterministic operation surfaces.

## Agent Runtime

These topics cover the agent-specific and AI infrastructure layers that sit above ordinary APIs.

- [Agent Protocols](./agent-protocols.md) - MCP, A2A, tasks, tools, resources, prompts, streaming, and agent capability exchange.
- [Memory](./memory.md) - Vector databases, RAG, knowledge graphs, embeddings, retrieval pipelines, and long-term state.
- [Models](./models.md) - Hosted models, local models, inference runtimes, gateways, model routing, and model selection.

## Application Layer

This topic covers the final product and workflow layer built from the lower stack.

- [Applications](./applications.md) - Research, coding, enterprise, and operational agents composed from discovery, identity, APIs, protocols, memory, and models.

## Related Pages

- [Technology Stack](/architecture/technology-stack) - The seven stack levels and how the topic guides map to them.
- [Glossary](/glossary) - Definitions for terms used across the topic guides.
- [Architecture Flows](/architecture/flows) - Diagrams showing how the layers work together.
