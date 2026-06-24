# Runnable Demo Roadmap

## Summary

The runnable demo milestone turns the reference documentation and machine-readable examples into a local demonstration platform.

## Current Capabilities

- FastAPI backend exposing `/openapi.json`, `/documents/search`, `/documents/{documentId}`, and `/reviews/drafts`.
- Public `/.well-known/agent-card.json` endpoint based on `specs/demo/agent-card.json`.
- Local JWT token helper for scoped demo access.
- Protocol-shaped MCP endpoint exposing `search_documents` and `fetch_document`.
- Protocol-shaped A2A endpoint accepting the demo `message/send` request.
- File-backed corpus for deterministic retrieval.
- Static graph-style related-document expansion.
- Mock model routing that creates deterministic review outlines.
- End-to-end example workflow under `examples/literature-review`.
- Trace ID propagation through `X-Trace-Id`, audit events, JSON-RPC metadata, and A2A task metadata.
- Local debug endpoints for runtime metadata and recent audit events.
- Native setup, doctor, and smoke-test commands without Docker or external services.

## Local Commands

```bash
npm run api:sync
npm run demo:doctor
npm run api:test
npm run demo:smoke
npm run api:dev
npm run demo:run
```

Use `npm run api:dev` in one terminal, then run `npm run demo:run` from another terminal.

## Quality Checks

- A developer can run the demo locally from documented commands.
- The smoke command starts the API on a free local port, runs the workflow, verifies the result, and shuts down cleanly.
- Discovery, OpenAPI, MCP, A2A, memory, and application examples align with the published demo specs.
- CI validates specs, runs backend tests, runs the smoke demo, and builds docs.
- No external model or identity provider is required for the default local demo.

## Recommended Demo Defaults

- Backend: FastAPI.
- Identity mode: local JWT validation fixture.
- Model mode: mock model gateway.
- Memory mode: local deterministic corpus before adding real vector database infrastructure.
