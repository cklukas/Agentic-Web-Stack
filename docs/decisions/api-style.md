# API Style

## Recommended Starting Point

Use **REST with OpenAPI 3.1** as the default service contract. Add GraphQL only when clients need flexible graph-shaped queries that would otherwise create too many REST endpoints.

## Tradeoffs

| Choice | Best fit | Strength | Cost |
| --- | --- | --- | --- |
| REST + OpenAPI | Tool-friendly service operations | Mature tooling, easy auth, clear operation IDs | Can overgrow for complex graph queries |
| GraphQL | Client-shaped domain queries | Efficient flexible reads | More complex caching, auth, and schema governance |
| JSON Schema | Shared payload validation | Reusable across APIs and tools | Does not define transport behavior |
| Event APIs | Asynchronous domain updates | Good for streaming system state | Harder for simple agent request/response tasks |

## Architecture Guidance

- Keep API operation IDs stable because agents and tool wrappers may depend on them.
- Publish authored or exported API contracts as machine-readable artifacts.
- Use JSON Schema-compatible request and response shapes where possible.
- Require auth scopes in the OpenAPI contract for protected operations.

## Example Artifact

- [openapi.yaml](/specs/demo/openapi.yaml)
