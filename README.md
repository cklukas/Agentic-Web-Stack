# Agentic Web Stack

Reference architectures, protocols, standards, and technologies for the emerging Agentic Web.

The web is evolving from a network of pages and APIs into a network of intelligent agents that can discover services, authenticate, communicate, delegate tasks, access tools, retrieve knowledge, and collaborate across organizational boundaries.

This project provides a documentation-first reference architecture for the Agentic Web Stack plus a deterministic local demo. It demonstrates how modern AI agents can be exposed, discovered, integrated, and operated using open standards and emerging protocols.

The goal is not to promote a specific vendor or framework, but to provide a clear and reproducible architecture that developers can use as a starting point for building agent-native systems.

## Documentation

This repository is documentation-first. The canonical project knowledge base lives in [`docs`](docs/index.md) and is built with [ckdocs](https://github.com/cklukas/ck-git-hosting), with navigation and site metadata in [`ckdocs.yml`](ckdocs.yml). With `ckdocs` on your `PATH`, preview it locally with live reload:

```bash
npm run docs:dev
```

`npm run docs:build` writes the static site to `public/` and fails on any broken
link, heading fragment or diagram.

Two workflows publish the same site with ckdocs 0.8.1, each only after that
strict validation: [`.github/workflows/docs.yml`](.github/workflows/docs.yml)
runs the spec and demo checks and deploys to
[GitHub Pages](https://cklukas.github.io/Agentic-Web-Stack/), and
[`.ckgit/ci.yml`](.ckgit/ci.yml) builds the pinned ckdocs source and publishes
the rpi4 copy, passing `--site-url` so its `llms.txt` links stay on that host.

Use the documentation site for architecture notes, technology stack levels, topic goals, standards, protocol references, papers, glossary terms, and runnable demo guidance.

Start with:

- [End-to-End Demo](docs/guides/end-to-end-demo.md)
- [Run the Local Demo](docs/guides/run-local-demo.md)
- [Technology Stack](docs/architecture/technology-stack.md)
- [Specifications](docs/specifications/index.md)
- [Security and Trust](docs/guides/security-trust.md)
- [Agent Card](docs/concepts/agent-card.md)
- [Agent2Agent](docs/concepts/a2a.md)
- [Model Context Protocol](docs/concepts/mcp.md)
- [Glossary](docs/glossary.md)

## Repository Structure

```text
docs/      Canonical documentation, published with ckdocs
specs/     Machine-readable specs, schemas, discovery documents, and API definitions
services/  Local FastAPI demo plus future backend, MCP, and A2A services
agents/    Future research, coding, and enterprise agent implementations
examples/  Runnable end-to-end examples and workflows
infra/     Future local orchestration, deployment, and infrastructure assets
```

## Local Demo

The runnable demo is a deterministic **Literature Review Assistant**. It exposes Agent Card discovery, local JWT access, OpenAPI REST endpoints, MCP-shaped tools, an A2A-shaped delegation endpoint, document retrieval, and review draft creation.

Prerequisites:

- Node.js 18 or newer
- npm
- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)

Install and test:

```bash
npm install
npm run api:sync
npm run demo:doctor
npm run api:test
npm run demo:smoke
```

Start the API:

```bash
npm run api:dev
```

In another terminal, run the workflow:

```bash
npm run demo:run
```

The API accepts and returns `X-Trace-Id` headers. Local debug endpoints are available at `/debug/runtime` and `/debug/audit-events` with the `debug:read` dev-token scope.

## What Is the Agentic Web?

The Agentic Web extends the traditional web with autonomous and semi-autonomous AI agents capable of:

- Discovering services and other agents
- Understanding capabilities
- Accessing tools and APIs
- Authenticating securely
- Delegating tasks
- Retrieving and storing knowledge
- Collaborating with humans and other agents

Just as websites became accessible through browsers, Agentic Web services become accessible through AI agents.

## Reference Architecture

```text
Layer 7  Applications
         Research Agents
         Coding Agents
         Enterprise Agents

Layer 6  Models
         OpenAI
         Gemini
         Claude
         Local LLMs

Layer 5  Memory
         Vector Database
         Knowledge Graph

Layer 4  Agent Protocols
         MCP
         A2A

Layer 3  APIs
         REST
         GraphQL
         OpenAPI

Layer 2  Identity
         OAuth2
         OpenID Connect

Layer 1  Discovery
         Agent Card
         robots.txt
         sitemap.xml
         llms.txt (proposal)
```

## Demonstration Platform

This repository contains documentation, validated demo specifications, and a local runnable demonstration platform consisting of the following components.

### Demo Website

A traditional website exposing:

- Human-readable documentation
- Agent documentation
- OpenAPI specification
- Discovery endpoints
- Authentication examples

### FastAPI Backend

A modern backend exposing:

- REST APIs
- OpenAPI schema
- Local JWT authentication
- Tool endpoints
- Agent services

### Agent Card

Machine-readable metadata describing:

- Agent identity
- Capabilities
- Available services
- Authentication requirements
- Supported protocols

Example:

```json
{
  "name": "Agentic Web Demo Agent",
  "description": "Reference implementation agent",
  "capabilities": [
    "search",
    "knowledge-retrieval",
    "task-execution"
  ]
}
```

## Discovery Layer

The discovery layer allows agents to find services and understand capabilities.

Examples:

```text
/.well-known/agent-card.json
/robots.txt
/sitemap.xml
/llms.txt  (optional documentation index proposal)
/openapi.json
```

Future standards and experiments can be added as the ecosystem evolves.

The [llms.txt concept](docs/concepts/llms-txt.md) describes an optional documentation entry point in this layer: a curated guide to context an agent can read before using services. It is documented as a community proposal; the local demo does not currently serve it.

## Identity Layer

Demonstrates secure authentication and authorization.

Technologies:

- OAuth2
- OpenID Connect
- JWT tokens

The goal is to show how agents can securely access protected resources while preserving user identity and permissions.

## API Layer

Provides multiple API styles commonly used in modern systems.

### REST

Traditional HTTP APIs.

### GraphQL

Flexible query-based access.

### OpenAPI

Machine-readable API definitions enabling automatic tool discovery and integration.

## Agent Protocol Layer

### Model Context Protocol

Demonstrates:

- Tool exposure
- Resource exposure
- Agent-to-tool communication

### Agent-to-Agent

Demonstrates:

- Agent discovery
- Capability exchange
- Task delegation
- Multi-agent workflows

## Memory Layer

Demonstrates long-term and semantic memory systems.

### Vector Database

Examples:

- Chroma
- Qdrant
- Weaviate

Used for:

- RAG
- Semantic search
- Context retrieval

### Knowledge Graph

Structured entity relationships for reasoning and navigation.

Examples:

- Neo4j
- RDF
- Property graphs

## Model Layer

Shows how different model providers can be integrated behind a common architecture.

Supported examples:

### Hosted Models

- OpenAI
- Gemini
- Claude

### Local Models

- Ollama
- llama.cpp
- vLLM

The architecture intentionally avoids vendor lock-in.

## Application Layer

Example applications built on top of the stack.

### Research Agent

Literature discovery, retrieval, summarization, and knowledge exploration.

### Coding Agent

Code generation, repository analysis, and development workflows.

### Enterprise Agent

Business process automation, data retrieval, and system integration.

## Project Goals

- Explain the emerging Agentic Web architecture
- Provide practical reference implementations
- Demonstrate interoperability between standards
- Help developers build agent-native systems
- Remain vendor-neutral and standards-focused

## Status

This project is an evolving exploration of the Agentic Web ecosystem.

As standards such as MCP, A2A, Agent Cards, discovery mechanisms, identity frameworks, and memory architectures mature, this repository will continue to expand with new examples and reference implementations.

Contributions, discussions, and alternative architectures are welcome.
