DEMO_ISSUER = "agentic-web-stack-demo"
DEMO_AUDIENCE = "agentic-web-stack"
DEMO_SECRET = "agentic-web-stack-local-demo-secret"
DEMO_ALGORITHM = "HS256"

DEFAULT_SCOPES = ["research:read", "drafts:write"]
DEBUG_SCOPE = "debug:read"
SUPPORTED_SCOPES = [*DEFAULT_SCOPES, DEBUG_SCOPE]

TRACE_HEADER = "X-Trace-Id"
