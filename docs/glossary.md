# Glossary

## A2A

[Agent2Agent](/concepts/a2a). An open protocol for communication, discovery, task delegation, and collaboration between independent AI agents.

## Agent

An AI-driven software component that can reason over context, use tools, interact with users or systems, and pursue tasks with some degree of autonomy.

## Agent Card

[Agent Card](/concepts/agent-card). A JSON metadata document that describes an agent's identity, endpoint, capabilities, skills, supported interfaces, and authentication requirements. In A2A, the well-known path is commonly `/.well-known/agent-card.json`.

## Agent Framework

[Agent framework](/concepts/framework-vs-protocol). A software framework for building agent applications, usually including orchestration, tool calling, memory integration, state management, and evaluation support.

## Agent Operations

The production operation of agent systems, including monitoring, evaluation, audit, cost control, policy enforcement, incident response, and lifecycle management.

## Agent Protocol

[Agent protocol](/topics/agent-protocols). A protocol designed for agent-specific interactions such as tool access, resource access, discovery, task delegation, streaming updates, and artifact exchange.

## Agent Skill

A task-oriented capability listed in an Agent Card. A skill usually includes an ID, name, description, input modes, output modes, and examples.

## API

Application Programming Interface. A deterministic software interface used by humans, applications, and agents to interact with a system.

## Artifact

An output produced by an agent task. Examples include text, files, structured data, reports, summaries, patches, or references.

## Capability

A declared function or feature that a service or agent can provide. Capabilities should be described in machine-readable metadata when possible.

## Capability Exchange

The process where agents or clients inspect metadata to understand supported skills, endpoints, protocols, authentication requirements, and operational limits before starting work.

## Audit

[Audit](/guides/operations-evaluation). The recording of security-relevant and operationally relevant events, such as who delegated access, which agent acted, which tools were called, and what artifacts were produced.

## Compliance Control

A technical or procedural control used to satisfy regulatory, contractual, security, privacy, or governance requirements.

## Delegation

[Delegation](/concepts/identity-delegation). The act of allowing an agent or service to act on behalf of a human, service account, organization, or another agent within explicit scopes and policy limits.

## Discovery

[Discovery](/topics/discovery). The process of finding services, agents, metadata, schemas, endpoints, and capabilities.

## Embedding

A numeric representation of text, images, or other content used for semantic similarity search and retrieval.

## Evaluation

[Evaluation](/concepts/evaluation). The process of testing an agent system for quality, correctness, safety, security, latency, reliability, or task completion against defined scenarios and expected outcomes.

## Gateway

An intermediary service that routes, secures, observes, transforms, or governs calls between clients and backend services, tools, models, or protocols.

## Graph

A data structure made of nodes and edges. In agent systems, graphs often represent entities, relationships, workflows, dependencies, or knowledge.

## GraphQL

A query language and execution model for APIs where clients can request precisely shaped data.

## Governed Discovery

[Governed discovery](/concepts/agent-discovery). Discovery that is constrained by policy, trust metadata, approval workflows, registries, or organizational controls rather than relying only on public metadata.

## Hosted Model API

A model API operated by an external provider or managed platform, typically accessed over HTTPS and billed by usage, capacity, or subscription.

## Hybrid Search

A retrieval pattern that combines semantic vector search with keyword, structured, graph, or metadata filters to improve relevance and precision.

## Identity

[Identity](/topics/identity). The layer that determines who or what is calling a system, who is being represented, and which actions are allowed.

## Interoperability

The ability for independently built systems, agents, tools, or services to exchange information and work together through shared protocols, schemas, identity, and operational expectations.

## JSON Schema

A vocabulary for describing, validating, and documenting JSON data structures.

## JWT

JSON Web Token. A compact token format often used to carry identity, authorization, or session claims.

## Knowledge Graph

A structured graph of entities and relationships used for navigation, reasoning, and context retrieval.

## llms.txt

[llms.txt](/concepts/llms-txt). A community proposal for a curated Markdown entry point to website documentation that agents can use as context. In this stack it belongs to Layer 1, Discovery.

## Local Inference

Running a model on infrastructure controlled by the developer or organization, rather than calling a hosted model API.

## Marketplace

A catalog where agents, tools, integrations, datasets, or capabilities can be discovered, evaluated, acquired, or enabled.

## MCP

[Model Context Protocol](/concepts/mcp). An open protocol for connecting AI applications and agents to tools, resources, and prompts.

## Memory

[Memory](/concepts/memory). State or context that persists beyond a single model call. Memory can include retrieved documents, embeddings, conversation state, user preferences, entities, relationships, and task history.

## Model API

A hosted or self-managed API used to call model capabilities such as text generation, embeddings, tool use, multimodal understanding, or structured output.

## Model Infrastructure

The runtime, serving, routing, deployment, observability, and governance systems used to operate models in applications.

## OIDC

[OpenID Connect](/topics/identity). The common acronym for the identity layer built on top of OAuth2.

## Origin

The historical source of a technology, such as its first public release, original developer, research project, standards body, or company announcement.

## OpenAPI

[OpenAPI](/concepts/agent-card-vs-openapi). A machine-readable description format for HTTP APIs. OpenAPI documents are commonly exposed as `openapi.json` or `openapi.yaml`.

## OAuth2

[OAuth2](/topics/identity) is an authorization framework used to grant scoped access to protected resources.

## OpenID Connect

[OpenID Connect](/topics/identity) is an identity layer on top of OAuth2 that lets clients verify end-user identity and receive profile claims.

## Operations

The practices and systems used to run agent applications in production, including deployment, monitoring, incident response, scaling, cost control, evaluation, and change management.

## Orchestration

[Orchestration](/concepts/framework-vs-protocol). The coordination of steps, tools, agents, model calls, state transitions, retries, and human review inside a workflow.

## Policy

[Policy](/guides/security-trust). A rule or decision layer that determines whether an action, delegation, data access, tool call, or protocol exchange is allowed.

## Protocol Gateway

A gateway that mediates protocol traffic, such as MCP or A2A, and adds controls such as authentication, authorization, validation, logging, rate limits, or routing.

## Production-Ready

Mature enough for real operational use, with sufficient stability, security, documentation, testing, observability, support, and governance for the intended environment.

## RAG

[Retrieval-Augmented Generation](/concepts/rag-vs-memory). A pattern where relevant external information is retrieved and supplied to a model as context.

## RDF

Resource Description Framework. A W3C standard data model for representing linked data as subject-predicate-object statements.

## Registry

[Registry](/concepts/agent-registry). A catalog or directory where agents, services, schemas, endpoints, metadata, or trust information can be published and discovered.

## Resource

In MCP, a URI-addressed context object exposed by a server. More generally, any retrievable data object used by an agent or service.

## REST

An HTTP API style centered on resources, methods, status codes, and representations.

## Retrieval

[Retrieval](/topics/memory). The process of finding relevant context from documents, databases, indexes, graphs, tools, or APIs for use by an agent or model.

## Serving Engine

Runtime software that hosts models and handles inference requests, batching, scheduling, memory management, streaming, and throughput optimization.

## SPARQL

A W3C query language for RDF graphs.

## Stateful Workflow

A workflow that preserves explicit state across steps, retries, human review, tool calls, or long-running agent tasks.

## Stewardship

The organization, foundation, standards body, company, university, or maintainer community responsible for evolving a technology after its initial creation.

## Task

In agent protocols, a unit of work that can have state, messages, artifacts, progress updates, and completion or failure outcomes.

## Tool

[Tool](/concepts/tool-use). A callable operation exposed to an agent or model, such as querying a database, calling an API, searching documents, or creating a ticket.

## Tool Calling

[Tool calling](/concepts/tool-use). The pattern where a model or agent selects and invokes an external tool using a structured request and then uses the tool result in later reasoning or output.

## Trust Profile

[Trust profile](/concepts/trust-model). A documented set of identity, security, governance, provenance, evaluation, and operational expectations used to decide whether an agent or service can be trusted.

## Vector Database

A database optimized for storing embeddings and performing similarity search.

## Web Foundation

A mature web standard, protocol, architecture style, or metadata convention that newer agent systems build on instead of replacing.

## Well-Known URI

A predictable URL path under `/.well-known/` used to publish metadata for discovery, configuration, or interoperability.
