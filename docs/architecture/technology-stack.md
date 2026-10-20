# Technology Stack

The Agentic Web Stack is organized as seven technology levels. A technology level is a boundary of responsibility: it explains what problem the layer solves, which artifacts it produces, and which technologies are commonly used in current implementations.

The layers are not product categories or vendor recommendations. They are a practical map for deciding where a tool belongs and how it should connect to the rest of the system.

## How to Read the Stack

- Start at the bottom when exposing a new agent or service: discovery, identity, APIs, then agent protocols.
- Start at the top when designing a product workflow: application goal, model needs, memory needs, then protocol and API integration.
- Use [Agentic Web Stack Timeline](/references/timeline) for the chronological development path, and [Technology Origins](/references/technology-origins) when you need the first public milestone, original developer, or stewardship model for a technology.
- Use [End-to-End Demo](/guides/end-to-end-demo), [Architecture Flows](/architecture/flows), and [Specifications](/specifications/) to see the stack as a complete scenario.

## Common Stack by Level

| Level | Responsibility | Common technologies | First docs |
| --- | --- | --- | --- |
| 7 Applications | User-facing workflows and task orchestration | LangGraph, CrewAI, Semantic Kernel, ADK, custom Python or TypeScript agents | [Applications](/topics/applications) |
| 6 Models | Reasoning, generation, embeddings, and multimodal inference | OpenAI, Gemini, Claude, Ollama, llama.cpp, vLLM, model gateways | [Models](/topics/models) |
| 5 Memory | Retrieval, semantic search, long-term state, structured knowledge | Chroma, Qdrant, Weaviate, pgvector, Neo4j, RDF, SPARQL | [Memory](/topics/memory) |
| 4 Agent Protocols | Agent-to-tool and agent-to-agent interoperability | MCP, A2A, JSON-RPC, protocol adapters, streaming transports | [Agent Protocols](/topics/agent-protocols) |
| 3 APIs | Deterministic service capabilities and schemas | REST, GraphQL, OpenAPI, JSON Schema, FastAPI, Express, NestJS, Spring Boot | [APIs](/topics/apis) |
| 2 Identity | Authentication, authorization, delegation, and policy | OAuth2, OpenID Connect, JWT, JWK, mTLS, API gateways, OPA | [Identity](/topics/identity) |
| 1 Discovery | Service, agent, and documentation metadata | Agent Card, `/.well-known/agent-card.json`, agent registries, OpenAPI, robots.txt, sitemap.xml, llms.txt (proposal) | [Discovery](/topics/discovery) |

## Level Introductions

### Level 1: Discovery

Discovery answers: "What exists here, what can it do, and how do I talk to it?" For agents, the key artifact is the Agent Card, usually published at `/.well-known/agent-card.json` for A2A-compatible agents. Registries add local trust metadata such as approved domains, versions, protocols, and review status. Traditional web discovery artifacts such as `robots.txt`, `sitemap.xml`, and `openapi.json` still matter because agents often combine web crawling, API inspection, and explicit agent metadata.

[llms.txt](/concepts/llms-txt) complements these artifacts with a curated documentation entry point. In an agentic OS, it can help an agent locate context before choosing tools, calling APIs, or retrieving knowledge. It is an optional community proposal; service contracts and trust decisions remain with the other stack components.

### Level 2: Identity

Identity answers: "Who is calling, who is being represented, and what is allowed?" Most production systems still use OAuth2, OpenID Connect, access tokens, scopes, claims, API gateways, and policy engines. Agent systems add delegation pressure: an agent may need to act for a human, a service account, or another agent while preserving auditability.

### Level 3: APIs

APIs answer: "Which deterministic operations can be called?" REST and GraphQL remain the common service surfaces. OpenAPI and JSON Schema make these APIs machine-readable so agents, SDK generators, test tools, and governance tools can inspect the contract.

### Level 4: Agent Protocols

Agent protocols answer: "How do agents use tools and collaborate with other agents?" MCP standardizes agent-to-tool and agent-to-resource access. A2A standardizes agent-to-agent communication, discovery, task delegation, and result exchange. These protocols sit above ordinary APIs but usually still rely on HTTP, JSON, authentication, and service infrastructure.

### Level 5: Memory

Memory answers: "What context should survive beyond one model call?" Vector databases support semantic retrieval and RAG. Knowledge graphs support explicit entity relationships and reasoning paths. Production systems often combine both with relational databases and object storage.

### Level 6: Models

Models answer: "Which inference capability should perform the reasoning or generation?" Hosted providers offer strong managed capabilities, while local runtimes offer control over deployment, privacy, cost, and latency. A mature stack keeps model choice replaceable where possible.

### Level 7: Applications

Applications answer: "What useful work does the system perform?" Research agents, coding agents, and enterprise agents compose every lower level: they discover services, authenticate, call APIs, use tools, retrieve memory, invoke models, and coordinate task state.

## Recommended Learning Path

1. Read [Agent Card](/concepts/agent-card) to understand agent self-description.
2. Read [A2A](/concepts/a2a) and [MCP](/concepts/mcp) to understand protocol boundaries.
3. Read [Discovery](/topics/discovery), [Identity](/topics/identity), and [APIs](/topics/apis) to understand the web substrate.
4. Read [Memory](/topics/memory), [Models](/topics/models), and [Applications](/topics/applications) to understand the agent runtime side.
5. Read [Agentic Web Stack Timeline](/references/timeline) for the development history, then [Technology Origins](/references/technology-origins) for dates, origin organizations, governance context, and reference links.
6. Read [End-to-End Demo](/guides/end-to-end-demo), [Security and Trust](/guides/security-trust), and [Operations and Evaluation](/guides/operations-evaluation) for a complete scenario and production-readiness concerns.
