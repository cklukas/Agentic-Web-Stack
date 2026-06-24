# APIs

## Topic Summary

The API layer exposes deterministic system capabilities that agents can inspect, call, test, and govern.

## Stack Level

APIs are Layer 3 of the Agentic Web Stack. They expose deterministic system operations below agent protocols. Agents may call APIs directly, or APIs may sit behind MCP tools, A2A services, or application-specific adapters.

## Goals

- Provide REST APIs with machine-readable OpenAPI descriptions.
- Document where GraphQL can be useful for flexible query access.
- Make API definitions reusable by humans, agents, and tooling.

## Common Tech Stack

| Technology | Role in APIs |
| --- | --- |
| REST over HTTP | Default integration style for service operations and resource access |
| GraphQL | Flexible query layer for clients that need shaped data from complex domains |
| OpenAPI | Machine-readable REST contract for discovery, SDK generation, testing, and governance |
| JSON Schema | Shared validation vocabulary for request, response, and event payloads |
| FastAPI | Python API framework with strong OpenAPI support |
| Express or NestJS | Common Node.js and TypeScript API stacks |
| Spring Boot | Common Java enterprise API stack |
| API gateways | Routing, auth enforcement, throttling, and observability |

## Reference Scenario

The Literature Review Assistant uses deterministic REST APIs for registry lookup, document search, document metadata, draft creation, and local trace inspection. These APIs can be called directly, wrapped as MCP tools, or used behind an A2A service.

## Related Materials

- [OpenAPI demo contract](/specs/demo/openapi.yaml)
- [API Style Decision](/decisions/api-style)
- [End-to-End Demo](/guides/end-to-end-demo)

## Standards and Protocols

- REST over HTTP
- OpenAPI
- JSON Schema
- GraphQL

## Example Use Case

A task agent needs deterministic access to documents. Instead of asking a model to infer database behavior, the backend exposes a typed API for search and retrieval. The API can later be wrapped as an MCP tool or called directly by an A2A service.

## Example OpenAPI Snippet

```yaml
openapi: 3.1.0
info:
  title: Agentic Web Demo API
  version: 0.1.0
paths:
  /documents/search:
    post:
      summary: Search approved documents
      operationId: searchDocuments
      security:
        - oidc: [documents:read]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [query]
              properties:
                query:
                  type: string
                limit:
                  type: integer
                  minimum: 1
                  maximum: 10
                  default: 5
      responses:
        "200":
          description: Matching document passages
          content:
            application/json:
              schema:
                type: object
                required: [results]
                properties:
                  results:
                    type: array
                    items:
                      type: object
                      required: [id, title, snippet]
                      properties:
                        id:
                          type: string
                        title:
                          type: string
                        snippet:
                          type: string
components:
  securitySchemes:
    oidc:
      type: openIdConnect
      openIdConnectUrl: https://auth.example.com/.well-known/openid-configuration
```

Example artifact: [openapi.yaml](/specs/demo/openapi.yaml).

## Reference Links and Papers

- [Technology Origins](/references/technology-origins) - Local reference page with origin and stewardship context for REST, OpenAPI, GraphQL, JSON Schema, and common API technologies.
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - Normative machine-readable contract format for HTTP APIs.
- [JSON Schema](https://json-schema.org/) - Schema vocabulary for validating and documenting JSON payloads.
- [GraphQL Specification](https://spec.graphql.org/) - Normative language and execution specification for GraphQL APIs.
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) - Core HTTP semantics used by REST APIs, gateways, caches, clients, and protocol adapters.
- [FastAPI documentation](https://fastapi.tiangolo.com/) - Python framework documentation for building API services with automatic OpenAPI output.

## Design Considerations

- Keep operation IDs stable because agents and tool wrappers may depend on them.
- Use clear request and response schemas for every agent-callable operation.
- Include security schemes and required scopes in the API description.
- Prefer deterministic API behavior for side effects and state changes.
