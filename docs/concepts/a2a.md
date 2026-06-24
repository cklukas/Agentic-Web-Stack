# Agent2Agent

Agent2Agent, usually shortened to A2A, is an open protocol for communication and interoperability between AI agents. It is intended for agents that may be built with different frameworks, hosted by different organizations, and operated as independent services.

A useful rule of thumb:

- Use A2A when one agent needs to discover, call, delegate to, or coordinate with another agent.
- Use MCP when an agent needs to access tools, resources, prompts, or external systems.

## Origin and Stewardship

A2A was publicly introduced by Google in 2025 to address interoperability between agents built with different vendors, frameworks, and deployment models. Google later donated the project to the Linux Foundation in June 2025 so the protocol could evolve under open governance rather than as a single-vendor interface.

The protocol reached a stable 1.0 milestone in 2026. Current A2A governance is organized around the Linux Foundation project and its technical steering committee. For architecture work, this matters because A2A should be treated as an emerging open interoperability layer, not as a Google-only API.

A2A does not replace HTTP APIs, OAuth2, OpenID Connect, OpenAPI, or MCP. It defines the agent-to-agent contract above those layers: how a remote agent is described, how tasks are submitted, how progress and artifacts are exchanged, and how clients understand supported capabilities.

## What A2A Solves

A2A defines a common language for agent collaboration. It helps answer:

- Which remote agents exist?
- What skills and capabilities do they provide?
- Which protocols and interfaces do they support?
- How does a client send a task?
- How are task state, streaming updates, artifacts, and errors represented?
- How are authentication and authorization requirements described?

## Core Building Blocks

| Building block | Role |
| --- | --- |
| Agent Card | JSON metadata document used for discovery and capability inspection |
| Agent Skill | Task-oriented capability description exposed by an agent |
| Task | Unit of work that can move through states over time |
| Message | Communication payload exchanged during a task or interaction |
| Artifact | Output produced by an agent, such as text, files, structured data, or references |
| Streaming or push updates | Mechanisms for long-running task progress and asynchronous results |

## Typical Flow

1. A client discovers an Agent Card from `/.well-known/agent-card.json`, a registry, or direct configuration.
2. The client evaluates skills, capabilities, interfaces, and security requirements.
3. The client obtains credentials if the agent requires authentication.
4. The client sends a task or message to the remote agent.
5. The remote agent processes the task and returns status, messages, and artifacts.
6. For long-running tasks, the client receives streaming or push updates.

## A2A and MCP Together

A2A and MCP are complementary:

- A2A connects agents to other agents.
- MCP connects an agent or AI application to tools, resources, and prompts.

An agent might expose itself through A2A while internally using MCP servers for GitHub, databases, document stores, search, or enterprise systems.

## Common Technology Stack

- Agent framework: LangGraph, CrewAI, Semantic Kernel, ADK, or custom orchestration.
- Transport and service layer: HTTP, JSON, streaming responses, webhook-style push updates.
- Discovery: Agent Card at `/.well-known/agent-card.json` or a registry.
- Identity: OAuth2, OpenID Connect, bearer tokens, mTLS, or enterprise gateway policy.
- Observability: request logs, task traces, token usage, latency, and error telemetry.

## Example Use Case

A coding agent finds a security review agent through its Agent Card and delegates a dependency audit. The coding agent keeps ownership of the user workflow, while the security agent owns the audit task and returns a structured artifact.

## Example A2A Message

This sketch uses the JSON-RPC binding shape commonly used for A2A `message/send` requests.

```json
{
  "jsonrpc": "2.0",
  "id": "req-lit-review-001",
  "method": "message/send",
  "params": {
    "message": {
      "messageId": "msg-lit-review-001",
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "Find recent papers about agent interoperability and create a cited literature review outline."
        }
      ]
    },
    "configuration": {
      "acceptedOutputModes": ["application/json", "text/plain"],
      "blocking": false
    },
    "metadata": {
      "scenario": "literature-review-assistant",
      "requestedBy": "demo-client-agent",
      "traceId": "trace-demo-001"
    }
  }
}
```

Example task response:

```json
{
  "task": {
    "id": "task-dependency-audit-001",
    "contextId": "ctx-security-review-001",
    "status": {
      "state": "TASK_STATE_WORKING"
    }
  }
}
```

Example artifact: [a2a-message-send.json](/specs/demo/a2a-message-send.json).

## References and Further Reading

- [A2A Protocol](https://a2a-protocol.org/latest/) - Official documentation home for the Agent2Agent protocol, including overview, specification, extensions, and community resources.
- [A2A Specification](https://a2a-protocol.org/latest/specification/) - Normative protocol reference for agent cards, skills, tasks, messages, artifacts, events, transports, and security schemes.
- [A2A Agent Discovery](https://a2a-protocol.org/latest/topics/agent-discovery/) - Official guide to Agent Cards, well-known discovery, registries, direct configuration, security, and caching.
- [A2A and MCP](https://a2a-protocol.org/latest/topics/a2a-and-mcp/) - Official explanation of how A2A and MCP fit together without solving the same problem.
- [Google announcement: Agent2Agent Protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) - Original Google announcement describing the interoperability problem A2A was designed to solve.
- [Google Cloud donates A2A to the Linux Foundation](https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/) - Stewardship announcement explaining the move from Google-originated project to Linux Foundation governance.
- [Linux Foundation A2A project launch](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents) - Foundation announcement for the Agent2Agent protocol project.
- [A2A v1.0 announcement](https://a2a-protocol.org/latest/announcing-1.0/) - Stable specification milestone and production-readiness announcement.
- [Agent Card](/concepts/agent-card) - Local concept page for the A2A discovery document.
- [Agent Protocols Topic](/topics/agent-protocols) - Local topic guide for MCP, A2A, and protocol architecture.
