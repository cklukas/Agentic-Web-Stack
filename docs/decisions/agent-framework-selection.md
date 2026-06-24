# Agent Framework Selection

## Recommended Starting Point

Keep the protocol boundaries independent of the orchestration framework. For stateful, inspectable, long-running workflows, **LangGraph** is a strong first framework to evaluate. For small demos or tightly controlled flows, custom orchestration can be clearer.

## Tradeoffs

| Choice | Best fit | Strength | Cost |
| --- | --- | --- | --- |
| Custom orchestration | Small demos and strict control | Simple dependencies and explicit flow | More hand-built state handling |
| LangGraph | Stateful workflows | Graph execution, checkpoints, human-in-the-loop patterns | Framework learning curve |
| CrewAI | Role-based multi-agent workflows | Convenient crew and flow abstractions | May hide lower-level protocol boundaries |
| Semantic Kernel | Microsoft/.NET enterprise environments | Strong enterprise SDK orientation | Best fit depends on platform stack |
| Google ADK | Google-oriented agent development | Agent tooling and deployment path | Newer framework surface |

## Architecture Guidance

- Do not let framework abstractions replace OpenAPI, MCP, or A2A contracts.
- Keep early workflows small enough to inspect end to end.
- Prefer explicit state transitions and trace IDs.
- Add framework abstractions only after protocol and API boundaries are clear.

## Example Artifact

- [application-workflow.yaml](/specs/demo/application-workflow.yaml)
