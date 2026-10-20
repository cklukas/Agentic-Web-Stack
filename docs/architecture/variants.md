# Architecture Variants

The seven-layer model is stable, but implementations can be small, enterprise-governed, local/private, or workflow-specific. These variants show which layers are mandatory and where teams usually add controls.

## Minimal Demo Stack

Use this when the goal is learning, local testing, or documentation examples.

| Layer | Minimal implementation |
| --- | --- |
| Discovery | Local Agent Card and registry artifact |
| Identity | Local dev token with scoped JWT claims |
| APIs | FastAPI REST endpoints and OpenAPI contract |
| Agent Protocols | MCP-shaped tools and A2A-shaped message/send |
| Memory | Deterministic corpus with modeled vector and graph config |
| Models | Static model-routing policy, no external provider |
| Applications | Literature review workflow requiring human review |

## Enterprise Governed Stack

Use this when agents cross team or organizational boundaries.

- Discovery uses signed or approved Agent Cards plus private registries.
- Optional [llms.txt indexes](/concepts/llms-txt) help agents find approved documentation; fetched links pass the same destination and content checks as other external sources.
- Identity uses enterprise OIDC, scoped delegation, policy gateways, and audit.
- APIs preserve OpenAPI contracts and compatibility rules.
- MCP and A2A traffic passes through gateways with validation and logging.
- Memory enforces data classification, retention, and tenant boundaries.
- Models are routed through approved gateways with usage and cost controls.
- Applications require evaluation suites, incident review, and human override.

## Local or Private Stack

Use this when data residency, network isolation, or cost control dominates.

- Discovery and registries stay inside a private network.
- A documentation `llms.txt` index can stay on the internal site too; its location does not make protected content public or bypass authentication.
- Identity uses local or enterprise identity providers.
- APIs, tools, memory, and models run on controlled infrastructure.
- Local inference and local vector or graph stores are preferred.
- External calls require explicit approval and traceable policy decisions.

## Research Workflow Stack

Use this when the primary artifact is a cited analysis, report, review, or decision memo.

- Discovery identifies approved research agents and document sources.
- A source's `llms.txt` can point to corpus guides and citation instructions before retrieval; it complements the document search API.
- Identity preserves the researcher, tenant, and allowed collections.
- APIs expose document search, document retrieval, and draft creation.
- MCP tools provide controlled access to sources.
- A2A delegates the literature-review task to a specialized agent.
- Memory combines semantic retrieval with graph expansion.
- Models draft content, but the application requires human review before sharing.

## Related Pages

- [Technology Stack](./technology-stack.md)
- [Architecture Flows](./flows.md)
- [Trust Model](/concepts/trust-model)
- [Run the Local Demo](/guides/run-local-demo)
