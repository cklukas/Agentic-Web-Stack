# Layer Model

The reference architecture is organized into seven layers. Each layer can evolve independently, but the layers should remain easy to compose.

Use the [Architecture Overview](./index.md) for the canonical diagram and [Technology Stack](./technology-stack.md) for common implementation technologies.

| Layer | Name | Purpose | Initial Examples |
| --- | --- | --- | --- |
| 7 | Applications | User-facing and organization-facing agent workflows | Research agents, coding agents, enterprise agents |
| 6 | Models | Hosted and local language model providers | OpenAI, Gemini, Claude, Ollama, llama.cpp, vLLM |
| 5 | Memory | Long-term, semantic, and structured knowledge | Vector databases, knowledge graphs |
| 4 | Agent Protocols | Agent-to-tool and agent-to-agent interoperability | MCP, A2A |
| 3 | APIs | Deterministic application and system interfaces | REST, GraphQL, OpenAPI |
| 2 | Identity | Authentication, authorization, delegation, and policy | OAuth2, OpenID Connect, JWT |
| 1 | Discovery | Machine-readable service and agent discovery | Agent Cards, robots.txt, sitemap.xml, OpenAPI |

## Layer Responsibilities

### Layer 1: Discovery

Agents need predictable ways to find services, understand capabilities, and locate machine-readable metadata.

### Layer 2: Identity

Agents need secure ways to act on behalf of users, organizations, or service accounts while preserving permissions and auditability.

### Layer 3: APIs

Agents need stable system interfaces that can be inspected, called, tested, and governed.

### Layer 4: Agent Protocols

Agents need protocols for tools, resources, prompts, capability exchange, task delegation, and multi-agent collaboration.

### Layer 5: Memory

Agents need durable retrieval systems for semantic search, RAG, entity relationships, and historical context.

### Layer 6: Models

Agents need model access through provider-neutral abstractions that allow hosted and local models to be swapped or combined.

### Layer 7: Applications

Applications compose the lower layers into useful workflows for research, software engineering, operations, and enterprise automation.
