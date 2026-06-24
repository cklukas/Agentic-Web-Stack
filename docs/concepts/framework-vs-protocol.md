# Framework vs Protocol

Agent frameworks and agent protocols solve different problems.

| Question | Framework | Protocol |
| --- | --- | --- |
| Main purpose | Build and orchestrate an application | Interoperate across boundaries |
| Controlled by | Application team | Specification, standard, or shared contract |
| Examples | LangGraph, CrewAI, Semantic Kernel, ADK | OpenAPI, MCP, A2A, OAuth2/OIDC |
| Change speed | Can change with application code | Must be stable for clients and partners |
| Architecture role | Productivity and control flow | Compatibility, governance, integration |

## Decision Rule

Choose frameworks for implementation productivity. Use protocols for boundaries that other teams, agents, clients, or organizations must understand.

## Related Pages

- [Agent Framework Selection](/decisions/agent-framework-selection)
- [Protocol Selection](/decisions/protocol-selection)
- [Applications topic](/topics/applications)
