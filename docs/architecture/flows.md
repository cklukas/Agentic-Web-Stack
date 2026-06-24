# Architecture Flows

These diagrams show how an agent-native system moves from discovery to application output. The Literature Review Assistant is used as the running example.

## Agent Card Discovery

```mermaid
sequenceDiagram
  participant Client as Client Agent
  participant Site as Research Domain
  participant Registry as Optional Registry

  Client->>Site: GET /.well-known/agent-card.json
  Site-->>Client: Public Agent Card
  Client->>Client: Validate domain, version, skills, and auth
  alt Registry is required
    Client->>Registry: Verify approved agent metadata
    Registry-->>Client: Trust decision
  end
```

## OAuth Delegated Access

```mermaid
sequenceDiagram
  participant User as Researcher
  participant App as Web App
  participant IdP as OIDC Provider
  participant API as Research API

  User->>App: Start literature review
  App->>IdP: Authorization request
  IdP-->>App: Authorization code
  App->>IdP: Exchange code for tokens
  IdP-->>App: Access token with research scopes
  App->>API: Call with bearer token
  API->>API: Validate issuer, audience, expiry, scope, tenant
  API-->>App: Scoped response
```

## MCP Tool Access

```mermaid
sequenceDiagram
  participant Host as Agent Host
  participant Client as MCP Client
  participant Server as MCP Server
  participant API as Document API

  Host->>Client: Need approved document search
  Client->>Server: tools/list
  Server-->>Client: search_documents, fetch_document
  Host->>Client: tools/call search_documents
  Client->>Server: Validated tool call
  Server->>API: Deterministic API request
  API-->>Server: Matching passages
  Server-->>Client: Tool result
  Client-->>Host: Context for model use
```

## A2A Task Delegation

```mermaid
sequenceDiagram
  participant Client as Client Agent
  participant Remote as Literature Review Agent
  participant Tools as Internal Tools

  Client->>Remote: message/send
  Remote-->>Client: Task accepted
  Remote->>Tools: Search, retrieve, summarize
  Tools-->>Remote: Sources and context
  Remote-->>Client: Task update
  Remote-->>Client: Draft outline artifact
```

## RAG and Knowledge Memory

```mermaid
flowchart TD
  Source["Source papers"] --> Chunk["Chunk and normalize"]
  Chunk --> Embed["Create embeddings"]
  Embed --> Vector["Vector index"]
  Chunk --> Graph["Knowledge graph"]
  Query["Research question"] --> Search["Semantic search"]
  Search --> Vector
  Vector --> Context["Retrieved passages"]
  Graph --> Context
  Context --> Model["Reasoning model"]
  Model --> Draft["Cited draft"]
```

## Full Stack Sequence

```mermaid
sequenceDiagram
  participant User as Researcher
  participant App as Literature Review App
  participant Registry as Agent Registry
  participant IdP as OIDC Provider
  participant Agent as A2A Research Agent
  participant MCP as MCP Server
  participant API as OpenAPI Service
  participant Memory as Vector and Graph Memory
  participant Model as Model Gateway
  participant Trace as Trace and Audit

  User->>App: Ask for literature review
  App->>Agent: Fetch Agent Card
  App->>Registry: Verify approved agent entry
  Registry-->>App: Trust level and allowed protocols
  App->>IdP: Authenticate and request scopes
  IdP-->>App: Scoped access token
  App->>Agent: A2A message/send
  Agent->>Trace: Record trace ID and policy result
  Agent->>MCP: Discover tools
  Agent->>MCP: Call search_documents
  MCP->>API: POST /documents/search
  API->>Memory: Retrieve passages and graph context
  Memory-->>API: Ranked context
  API-->>MCP: Search results
  MCP-->>Agent: Tool result
  Agent->>Model: Draft cited outline
  Model-->>Agent: Draft content
  Agent->>API: POST /reviews/drafts
  API-->>Agent: Draft ID and review URL
  API->>Trace: Record draft artifact reference
  Agent-->>App: A2A artifact
  App-->>User: Review required
```
