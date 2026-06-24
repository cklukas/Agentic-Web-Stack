# End-to-End Demo

This guide follows a **Literature Review Assistant** that helps a researcher find papers, retrieve context, compare evidence, and create a draft that requires human review.

The scenario is a reference architecture example. It shows the contracts and flow a production system would need without depending on a specific vendor or framework.

## Scenario

A researcher asks:

> Find recent papers about agent interoperability, compare the main protocol approaches, and create a cited literature review outline.

The system must discover the research agent, authenticate the user, call deterministic APIs, delegate a task through A2A, use MCP tools for document access, retrieve memory, route model calls, and create a review draft.

A runnable local version of this flow is available in [Run the Local Demo](/guides/run-local-demo).

## Flow

1. The client reads the public [Agent Card](/specs/demo/agent-card.json).
2. The client checks the [agent registry entry](/specs/demo/agent-registry.yaml) for trust metadata.
3. The user authenticates through the [OIDC client configuration](/specs/demo/oidc-client.example.json).
4. The agent inspects the [OpenAPI contract](/specs/demo/openapi.yaml).
5. The client sends an [A2A message](/specs/demo/a2a-message-send.json).
6. The coordinator agent uses [MCP tools](/specs/demo/mcp-tools.json).
7. The agent retrieves context with the [memory configuration](/specs/demo/memory.yaml).
8. The runtime chooses models using the [model routing policy](/specs/demo/model-routing.yaml).
9. The application follows the [workflow definition](/specs/demo/application-workflow.yaml).
10. The workflow is checked against [evaluation scenarios](/specs/demo/evaluation-scenarios.yaml).

## Stack Mapping

| Layer | Scenario responsibility | Example artifact |
| --- | --- | --- |
| Discovery | Publish agent identity, skills, endpoints, and auth requirements | [agent-card.json](/specs/demo/agent-card.json) |
| Discovery and Trust | Confirm approved domain, trust level, protocol allowance, and review status | [agent-registry.yaml](/specs/demo/agent-registry.yaml) |
| Identity | Preserve user identity and delegated scopes | [oidc-client.example.json](/specs/demo/oidc-client.example.json) |
| APIs | Expose deterministic document and draft operations | [openapi.yaml](/specs/demo/openapi.yaml) |
| Agent Protocols | Delegate work and expose tools | [a2a-message-send.json](/specs/demo/a2a-message-send.json), [mcp-tools.json](/specs/demo/mcp-tools.json) |
| Memory | Retrieve semantic and graph context | [memory.yaml](/specs/demo/memory.yaml) |
| Models | Route reasoning, summarization, classification, and embeddings | [model-routing.yaml](/specs/demo/model-routing.yaml) |
| Applications | Compose the user-facing workflow | [application-workflow.yaml](/specs/demo/application-workflow.yaml) |

## Related Documentation

- [Technology Stack](/architecture/technology-stack) explains the seven stack levels.
- [Run the Local Demo](/guides/run-local-demo) executes this scenario against the local FastAPI service.
- [Architecture Flows](/architecture/flows) renders the protocol and system diagrams.
- [Security and Trust](/guides/security-trust) documents the security model.
- [Operations and Evaluation](/guides/operations-evaluation) defines production-readiness checks.
- [Specifications](/specifications/) lists every machine-readable example artifact.
- [Protocol Selection](/decisions/protocol-selection) explains when to use A2A, MCP, or direct APIs.

## What This Demonstrates

The scenario shows how the stack fits together as a user-facing workflow: discovery tells the client what exists, identity constrains access, APIs expose deterministic operations, agent protocols coordinate work, memory supplies context, models draft output, and application controls keep the human in the loop.

## Runtime Evidence

The local demo can print an ordered architecture trace:

```bash
npm run demo:run -- --show-trace
```

The trace is generated from audit-safe events and includes the stack layer, component, policy result, and safe artifact references for each observed step.
