# Model Deployment

## Recommended Starting Point

Use a **model gateway abstraction** with hosted primary routes for reasoning and summarization, a local route for private classification, and explicit cost/latency budgets.

## Tradeoffs

| Choice | Best fit | Strength | Cost |
| --- | --- | --- | --- |
| Hosted model API | Strong managed capability | Fast adoption, high-quality models | Provider dependency and data boundary review |
| Local runtime | Privacy, offline, cost control | Data stays in local environment | Ops burden and capability limits |
| vLLM-style serving | High-throughput self-hosting | Efficient serving for production workloads | Requires model hosting expertise |
| Model gateway | Multi-provider routing | Central logging, fallback, budgets | Extra component and policy surface |
| Direct SDK calls | Small prototypes | Minimal abstraction | Harder to swap providers later |

## Architecture Guidance

- Route by task type, not by provider name in application code.
- Record usage and latency per route.
- Keep raw prompts out of logs unless an explicit evaluation environment allows it.
- Define fallback behavior before deploying automated workflows.

## Example Artifact

- [model-routing.yaml](/specs/demo/model-routing.yaml)
