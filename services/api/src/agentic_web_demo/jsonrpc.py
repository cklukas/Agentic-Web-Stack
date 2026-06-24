from typing import Any

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from .context import get_trace_id


def json_rpc_metadata(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    metadata = {"traceId": get_trace_id()}
    if extra:
        metadata.update(extra)
    return metadata


def json_rpc_result(request_id: Any, result: dict[str, Any], metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result,
        "meta": json_rpc_metadata(metadata)
    }


def json_rpc_error(
    request_id: Any,
    code: int,
    message: str,
    data: dict[str, Any] | None = None,
    status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    error: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return JSONResponse(
        status_code=status_code,
        content={
            "jsonrpc": "2.0",
            "id": request_id,
            "error": error,
            "meta": json_rpc_metadata()
        }
    )


def validate_json_rpc(payload: dict[str, Any]) -> tuple[Any, str]:
    request_id = payload.get("id")
    method = payload.get("method")
    if payload.get("jsonrpc") != "2.0" or request_id is None or not isinstance(method, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_json_rpc", "detail": "Expected JSON-RPC 2.0 request with id and method."}
        )
    return request_id, method
