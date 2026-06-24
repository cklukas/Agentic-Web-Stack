from contextvars import ContextVar
from uuid import uuid4

from .config import TRACE_HEADER

_trace_id: ContextVar[str | None] = ContextVar("trace_id", default=None)


def new_trace_id() -> str:
    return f"trace-{uuid4().hex[:16]}"


def normalize_trace_id(value: str | None) -> str:
    if not value:
        return new_trace_id()

    stripped = value.strip()
    if not stripped or len(stripped) > 128:
        return new_trace_id()

    return stripped


def set_trace_id(trace_id: str):
    return _trace_id.set(trace_id)


def reset_trace_id(token) -> None:
    _trace_id.reset(token)


def get_trace_id() -> str:
    return _trace_id.get() or "trace-local"


__all__ = ["TRACE_HEADER", "get_trace_id", "new_trace_id", "normalize_trace_id", "reset_trace_id", "set_trace_id"]
