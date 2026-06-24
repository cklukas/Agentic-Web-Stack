# Evaluation

Evaluation checks whether an agent system behaves correctly, safely, and observably across expected and adverse scenarios.

For agentic systems, evaluation must cover protocol behavior, authorization failures, tool failures, stale discovery metadata, prompt injection, and human review controls.

## Evaluation Dimensions

| Dimension | Example check |
| --- | --- |
| Task success | Happy path produces the expected artifact |
| Authorization | Missing scopes block side effects |
| Tool reliability | Tool timeout returns a safe partial result |
| Retrieval safety | Prompt injection in sources does not expose secrets |
| Discovery governance | Stale Agent Card metadata is rejected |
| Observability | Trace and audit events explain the workflow |

## Demo Mapping

The demo scenarios are defined in [evaluation-scenarios.yaml](/specs/demo/evaluation-scenarios.yaml) and exercised by API tests.

The local trace endpoint turns runtime events into architecture evidence:

```text
GET /debug/traces/{traceId}
```

## Related Pages

- [Operations and Evaluation](/guides/operations-evaluation)
- [Trust Model](./trust-model.md)
- [Run the Local Demo](/guides/run-local-demo)
