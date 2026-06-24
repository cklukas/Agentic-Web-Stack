# Applications

## Topic Summary

The application layer composes discovery, identity, APIs, protocols, memory, and models into useful agent workflows.

## Stack Level

Applications are Layer 7 of the Agentic Web Stack. They are the user-facing or organization-facing workflows that combine every lower layer into useful work: discover services, authenticate, call APIs, use protocols, retrieve memory, invoke models, and return auditable results.

## Goals

- Demonstrate complete workflows instead of isolated protocol fragments.
- Provide example applications for research, coding, and enterprise automation.
- Keep examples small enough to inspect and reproduce.

## Common Tech Stack

| Technology | Role in applications |
| --- | --- |
| LangGraph | Stateful graph-based agent orchestration and human-in-the-loop workflows |
| CrewAI | Multi-agent workflow orchestration with roles, crews, and flows |
| Semantic Kernel | Enterprise-oriented agent and orchestration SDK across .NET, Python, and Java ecosystems |
| Google ADK | Code-first agent development kit for building and deploying agents |
| Custom Python or TypeScript | Lightweight choice when framework abstractions are too heavy |
| Observability tools | Traces, tool-call logs, token usage, latency, errors, and task state |
| Release automation and evaluation | Regression tests, prompt tests, integration tests, deployment automation |

## Reference Scenario

The Literature Review Assistant composes discovery, identity, APIs, A2A, MCP, memory, and model routing into a single user-facing workflow with human review before external side effects.

## Related Materials

- [End-to-End Demo](/guides/end-to-end-demo)
- [Agent Framework Selection Decision](/decisions/agent-framework-selection)
- [Operations and Evaluation](/guides/operations-evaluation)

## Standards and Protocols

- Agent discovery and capability exchange
- Authenticated API access
- Tool and resource access through agent protocols
- Retrieval and memory integration

## Example Use Case

A literature review application helps a researcher find recent work, inspect evidence, and produce a cited draft. The application is not only a chat interface: it composes discovery, identity, APIs, A2A, MCP, memory, and model routing into one auditable workflow.

## Example Application Workflow

```yaml
application: literature-review-assistant
entrypoint:
  type: web-app
  userRole: researcher
workflow:
  - id: authenticate
    layer: identity
    action: start_oidc_login
    scopes:
      - research:read
      - drafts:write
  - id: discoverResearchAgent
    layer: discovery
    action: fetch_agent_card
    url: https://research.example.edu/.well-known/agent-card.json
  - id: delegateSearch
    layer: agent-protocols
    protocol: a2a
    skill: paper-search
  - id: retrieveContext
    layer: memory
    action: vector_search_and_graph_expand
  - id: draftSummary
    layer: models
    route: reasoning
  - id: createDraft
    layer: apis
    operationId: createReviewDraft
humanControls:
  requireApprovalBefore:
    - createDraft
    - sendExternalEmail
observability:
  traceId: required
  recordToolCalls: true
  recordTokenUsage: true
```

Example artifact: [application-workflow.yaml](/specs/demo/application-workflow.yaml).

## Reference Links and Papers

- [Technology Origins](/references/technology-origins) - Local reference page with origin and stewardship context for common agent frameworks and related infrastructure.
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) - Paper describing the reasoning-plus-action pattern used by many tool-using agents.
- [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) - Paper exploring how language models can learn API/tool usage.
- [SWE-bench](https://arxiv.org/abs/2310.06770) - Software engineering benchmark based on real GitHub issues.
- [WebArena](https://arxiv.org/abs/2307.13854) - Benchmark environment for autonomous web agents.
- [LangGraph](https://www.langchain.com/langgraph) - LangChain framework for stateful graph-based agent orchestration.
- [CrewAI documentation](https://docs.crewai.com/) - Documentation for multi-agent crews, flows, memory, guardrails, and observability.
- [Semantic Kernel Agent Framework](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/) - Microsoft documentation for Semantic Kernel agent abstractions.
- [Agent Development Kit](https://adk.dev/) - Google ADK documentation for building, evaluating, and deploying agents.

## Design Considerations

- Keep the user-facing workflow tied to concrete lower-layer capabilities.
- Make human approval explicit before publishing, sending, deleting, or sharing content.
- Preserve trace IDs across discovery, auth, API calls, tools, model calls, and artifacts.
- Choose orchestration frameworks without hiding protocol boundaries.
