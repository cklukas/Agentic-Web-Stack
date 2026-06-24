import hashlib
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response, status
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from . import __version__
from .audit import audit, audit_events, trace_events
from .auth import create_dev_token, enforce_scopes, require_scopes, require_token
from .config import DEBUG_SCOPE, DEFAULT_SCOPES, SUPPORTED_SCOPES, TRACE_HEADER
from .context import get_trace_id, normalize_trace_id, reset_trace_id, set_trace_id
from .corpus import (
    approved_excerpts,
    document_by_id,
    expand_related_documents,
    load_documents,
    public_document,
    search_documents
)
from .jsonrpc import json_rpc_error, json_rpc_result, validate_json_rpc
from .models import (
    AuditEventsResponse,
    CreateReviewDraftRequest,
    DevTokenResponse,
    DocumentResponse,
    DocumentSearchRequest,
    DocumentSearchResponse,
    HealthResponse,
    ReviewDraft,
    RuntimeDebugResponse,
    TraceResponse
)
from .specs import (
    a2a_message_send_spec,
    agent_card_spec,
    agent_registry_spec,
    local_agent_card,
    local_agent_registry_entry,
    local_openapi,
    mcp_tools_spec,
    openapi_spec
)
from .workflow import create_draft, outline_from_results

app = FastAPI(
    title="Agentic Web Demo API",
    version=__version__,
    docs_url="/api-docs",
    redoc_url=None,
    openapi_url=None
)


def base_url(request: Request) -> str:
    return str(request.base_url).rstrip("/")


@app.middleware("http")
async def trace_middleware(request: Request, call_next):
    trace_id = normalize_trace_id(request.headers.get(TRACE_HEADER))
    token = set_trace_id(trace_id)
    request.state.trace_id = trace_id
    try:
        response = await call_next(request)
    finally:
        reset_trace_id(token)

    response.headers[TRACE_HEADER] = trace_id
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail, headers=exc.headers)
    return JSONResponse(status_code=exc.status_code, content={"error": "http_error", "detail": str(exc.detail)})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    return await request_validation_exception_handler(request, exc)


@app.get("/health", response_model=HealthResponse)
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "literature-review-assistant",
        "version": __version__
    }


@app.get("/.well-known/openid-configuration")
def openid_configuration(request: Request) -> dict[str, Any]:
    origin = base_url(request)
    return {
        "issuer": "agentic-web-stack-demo",
        "token_endpoint": f"{origin}/auth/dev-token",
        "jwks_uri": f"{origin}/.well-known/jwks.json",
        "response_types_supported": ["token"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["HS256"],
        "scopes_supported": SUPPORTED_SCOPES
    }


@app.get("/.well-known/jwks.json")
def jwks() -> dict[str, list[Any]]:
    return {"keys": []}


@app.get("/.well-known/agent-card.json")
def agent_card(request: Request) -> Response:
    card = local_agent_card(base_url(request))
    etag = f'W/"agent-card-{card["version"]}"'
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)
    audit(
        "agent_card_discovery",
        artifactRefs=["spec:agent-card.json"],
        agent_id="literature-review-assistant",
        agent_card_version=card["version"]
    )
    return JSONResponse(
        card,
        headers={
            "Cache-Control": "public, max-age=60",
            "ETag": etag
        }
    )


@app.get("/openapi.json")
def openapi(request: Request) -> dict[str, Any]:
    audit("openapi_contract_served", artifactRefs=["spec:openapi.yaml"])
    return local_openapi(base_url(request))


@app.get("/registry/agents/{agent_id}")
def registry_agent(agent_id: str, request: Request) -> dict[str, Any]:
    entry = local_agent_registry_entry(base_url(request), agent_id)
    if not entry:
        audit(
            "agent_registry_lookup",
            agent_id=agent_id,
            policyResult="denied",
            reason="unknown_agent"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "detail": "Agent registry entry not found."}
        )

    audit(
        "agent_registry_lookup",
        agent_id=agent_id,
        trust_level=entry["trustLevel"],
        artifactRefs=["spec:agent-registry.yaml"]
    )
    return entry


@app.get("/auth/dev-token", response_model=DevTokenResponse)
def dev_token(scope: Annotated[list[str] | None, Query()] = None) -> dict[str, Any]:
    scopes = scope or DEFAULT_SCOPES
    unsupported_scopes = sorted(set(scopes) - set(SUPPORTED_SCOPES))
    if unsupported_scopes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "unsupported_scope",
                "detail": f"Unsupported demo scopes: {', '.join(unsupported_scopes)}"
            }
        )

    token = create_dev_token(scopes)
    audit("dev_token_issued", scopes=scopes)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 3600,
        "scope": " ".join(scopes)
    }


@app.post("/documents/search", response_model=DocumentSearchResponse)
def document_search(
    payload: DocumentSearchRequest,
    _: Annotated[dict[str, Any], Depends(require_scopes(["research:read"]))]
) -> dict[str, Any]:
    results = search_documents(payload.query, payload.year_from, payload.limit)
    audit("documents_search", query=payload.query, result_count=len(results))
    return {"results": results}


@app.get("/documents/{document_id}", response_model=DocumentResponse)
def document_retrieve(
    document_id: str,
    _: Annotated[dict[str, Any], Depends(require_scopes(["research:read"]))]
) -> dict[str, Any]:
    document = document_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "detail": "Document not found."}
        )
    return public_document(document)


@app.post("/reviews/drafts", status_code=status.HTTP_201_CREATED, response_model=ReviewDraft)
def review_draft_create(
    payload: CreateReviewDraftRequest,
    request: Request,
    _: Annotated[dict[str, Any], Depends(require_scopes(["drafts:write"]))]
) -> dict[str, Any]:
    return create_draft(payload, base_url(request))


@app.get("/debug/runtime", response_model=RuntimeDebugResponse)
def debug_runtime(
    _: Annotated[dict[str, Any], Depends(require_scopes([DEBUG_SCOPE]))]
) -> dict[str, Any]:
    agent_card = agent_card_spec()
    registry = agent_registry_spec()
    api_spec = openapi_spec()
    mcp_spec = mcp_tools_spec()
    a2a_spec = a2a_message_send_spec()
    return {
        "service": "literature-review-assistant",
        "version": __version__,
        "corpusCount": len(load_documents()),
        "supportedScopes": SUPPORTED_SCOPES,
        "specs": {
            "agentCardVersion": agent_card["version"],
            "agentRegistryVersion": registry["registry"]["version"],
            "openapiVersion": api_spec["info"]["version"],
            "mcpTools": [tool["name"] for tool in mcp_spec["result"]["tools"]],
            "a2aMethod": a2a_spec["method"]
        }
    }


@app.get("/debug/audit-events", response_model=AuditEventsResponse)
def debug_audit_events(
    _: Annotated[dict[str, Any], Depends(require_scopes([DEBUG_SCOPE]))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50
) -> dict[str, Any]:
    return {"events": audit_events[-limit:]}


@app.get("/debug/traces/{trace_id}", response_model=TraceResponse)
def debug_trace(
    trace_id: str,
    _: Annotated[dict[str, Any], Depends(require_scopes([DEBUG_SCOPE]))]
) -> dict[str, Any]:
    return {"traceId": trace_id, "events": trace_events(trace_id)}


def parse_mcp_limit(request_id: Any, raw_limit: Any) -> int | JSONResponse:
    try:
        limit = int(raw_limit)
    except (TypeError, ValueError):
        return json_rpc_error(request_id, -32602, "limit must be an integer.")

    if limit < 1 or limit > 10:
        return json_rpc_error(request_id, -32602, "limit must be between 1 and 10.")

    return limit


@app.post("/mcp", response_model=None)
def mcp_endpoint(
    payload: dict[str, Any],
    _: Annotated[dict[str, Any], Depends(require_scopes(["research:read"]))]
) -> dict[str, Any] | JSONResponse:
    request_id, method = validate_json_rpc(payload)
    if method == "tools/list":
        spec = mcp_tools_spec()
        audit("mcp_tools_list", tool_count=len(spec["result"]["tools"]))
        return json_rpc_result(request_id, spec["result"])

    if method != "tools/call":
        return json_rpc_error(request_id, -32601, f"Unsupported MCP method: {method}.")

    params = payload.get("params")
    if not isinstance(params, dict) or not isinstance(params.get("name"), str):
        return json_rpc_error(request_id, -32602, "tools/call requires params.name.")

    name = params["name"]
    arguments = params.get("arguments") if isinstance(params.get("arguments"), dict) else {}
    audit("mcp_tool_call", tool=name)

    if name == "search_documents":
        query = str(arguments.get("query", ""))
        parsed_limit = parse_mcp_limit(request_id, arguments.get("limit", 5))
        if isinstance(parsed_limit, JSONResponse):
            return parsed_limit
        return json_rpc_result(
            request_id,
            {"content": [{"type": "json", "json": {"results": search_documents(query, limit=parsed_limit)}}]}
        )

    if name == "fetch_document":
        document_id = str(arguments.get("documentId", ""))
        if document_id == "timeout":
            audit("mcp_tool_failure", tool=name, document_id=document_id, retryAttempted=True)
            return json_rpc_error(
                request_id,
                -32002,
                "Document retrieval timed out.",
                {
                    "errorCategory": "tool_timeout",
                    "retryAttempted": True,
                    "userVisibleStatus": "partial_result",
                    "createsDraft": False
                }
            )
        document = document_by_id(document_id)
        if not document:
            return json_rpc_error(request_id, -32004, "Document not found.", {"documentId": document_id})
        return json_rpc_result(
            request_id,
            {
                "content": [
                    {
                        "type": "json",
                        "json": {
                            "documentId": document["documentId"],
                            "title": document["title"],
                            "sourceUrl": document["sourceUrl"],
                            "excerpts": approved_excerpts(document)
                        }
                    }
                ]
            }
        )

    return json_rpc_error(request_id, -32601, f"Unknown MCP tool: {name}.")


@app.post("/a2a/v1", response_model=None)
def a2a_endpoint(
    payload: dict[str, Any],
    request: Request,
    token: Annotated[dict[str, Any], Depends(require_token)]
) -> dict[str, Any] | JSONResponse:
    request_id, method = validate_json_rpc(payload)
    if method != "message/send":
        return json_rpc_error(request_id, -32601, f"Unsupported A2A method: {method}.")

    params = payload.get("params")
    if not isinstance(params, dict):
        return json_rpc_error(request_id, -32602, "message/send requires params.")

    metadata = params.get("metadata")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("requiredScopes"), list):
        return json_rpc_error(
            request_id,
            -32602,
            "message/send requires metadata.requiredScopes.",
            {"errorCategory": "missing_scope_metadata"}
        )

    agent_card_version = metadata.get("agentCardVersion")
    current_version = a2a_message_send_spec()["params"]["metadata"].get("expectedAgentCardVersion", "0.2.0")
    if agent_card_version and agent_card_version != current_version:
        audit("stale_agent_card", supplied_version=agent_card_version, expected_version=current_version)
        return json_rpc_error(
            request_id,
            -32010,
            "Stale discovery metadata.",
            {
                "errorCategory": "stale_discovery_metadata",
                "revalidatesDiscovery": True,
                "honorsCacheHeaders": True,
                "blocksUnsupportedProtocol": True,
                "expectedVersion": current_version
            }
        )

    required_scopes = [str(scope) for scope in metadata["requiredScopes"]]
    enforce_scopes(token, required_scopes)

    message = params.get("message") if isinstance(params.get("message"), dict) else {}
    parts = message.get("parts") if isinstance(message.get("parts"), list) else []
    question = " ".join(str(part.get("text", "")) for part in parts if isinstance(part, dict)).strip()
    if not question:
        return json_rpc_error(request_id, -32602, "message.parts must include text content.")

    results = search_documents(question, year_from=2023, limit=5)
    related_ids = expand_related_documents([result["documentId"] for result in results])
    outline = outline_from_results(question, results)
    source_document_ids = [result["documentId"] for result in results[:3]] or related_ids[:1] or [
        "doc-agent-card-2025"
    ]
    draft = create_draft(
        CreateReviewDraftRequest(
            topic=question,
            sourceDocumentIds=source_document_ids,
            outline=outline,
            humanReviewRequired=True
        ),
        base_url(request)
    )
    trace_id = get_trace_id()
    audit("a2a_message_send", result_count=len(results), draft_id=draft["draftId"])

    task_id = "task-" + hashlib.sha256(f"{request_id}|{question}".encode("utf-8")).hexdigest()[:12]
    return json_rpc_result(
        request_id,
        {
            "taskId": task_id,
            "status": {"state": "completed"},
            "artifacts": [
                {
                    "name": "literature-review-outline",
                    "parts": [
                        {
                            "kind": "data",
                            "data": {
                                "question": question,
                                "outline": outline,
                                "citations": results[:5],
                                "relatedDocumentIds": related_ids,
                                "draft": draft
                            }
                        }
                    ]
                }
            ],
            "metadata": {
                "traceId": trace_id,
                "callsMcpTools": ["search_documents", "fetch_document"],
                "createsDraft": True,
                "requiresHumanReview": True
            }
        }
    )
