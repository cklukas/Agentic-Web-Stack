# Operations and Evaluation

Agentic systems need to be observable, testable, and safe to change. This page defines an operating model for the Literature Review Assistant scenario and similar agent-native workflows.

## Observability

| Signal | Why it matters |
| --- | --- |
| Trace ID | Connects user request, discovery, auth, API calls, MCP tools, A2A task state, model calls, and draft creation |
| Structured logs | Supports debugging without scraping unstructured model transcripts |
| Tool call records | Shows which tools were invoked, with which inputs, and under which policy |
| Token and cost usage | Tracks model spend and prevents runaway workflows |
| Latency budgets | Distinguishes slow APIs, slow tools, slow retrieval, and slow model calls |
| Policy decisions | Explains why a call was allowed, denied, or required approval |
| Artifact metadata | Records source documents and draft provenance |

The local demo exposes a normalized trace at `GET /debug/traces/{traceId}`. Each trace event includes the stack layer, component, policy result, and safe artifact references.

## Evaluation Scenarios

The example evaluation file is [evaluation-scenarios.yaml](/specs/demo/evaluation-scenarios.yaml).

Baseline evaluations:

- Happy path literature review.
- Missing scope blocks draft creation.
- Prompt injection in retrieved text does not reveal secrets or bypass tool policy.
- MCP tool timeout returns a partial result and does not create a draft.
- Stale Agent Card triggers discovery revalidation.

## Release Readiness

Before an agent service is exposed to users or other agents:

- Machine-readable specs remain valid.
- Public documentation matches the exposed contracts.
- OpenAPI changes preserve operation IDs unless intentionally versioned.
- Agent Card version changes are documented.
- MCP tool schemas are backwards compatible or versioned.
- A2A task behavior is covered by at least one evaluation scenario.
- Logs include trace ID, user or service subject, tenant, tool name, model route, and policy result.
- Secrets and access tokens are absent from logs, artifacts, prompts, and stored memory.

## Incident Review Questions

- Which user, tenant, agent, and scopes were involved?
- Which Agent Card version and endpoint were used?
- Which tools and APIs were called?
- Which retrieved sources entered model context?
- Which policy decision allowed or blocked each side effect?
- Which model route was used and what was the fallback behavior?
- Did human approval happen before any external side effect?

## Example Artifacts

- [application-workflow.yaml](/specs/demo/application-workflow.yaml)
- [model-routing.yaml](/specs/demo/model-routing.yaml)
- [evaluation-scenarios.yaml](/specs/demo/evaluation-scenarios.yaml)
- [agent-registry.yaml](/specs/demo/agent-registry.yaml)
