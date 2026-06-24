from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import jwt
from fastapi import Header, HTTPException, status

from .audit import audit
from .config import DEMO_ALGORITHM, DEMO_AUDIENCE, DEMO_ISSUER, DEMO_SECRET, DEFAULT_SCOPES


def create_dev_token(scopes: list[str] | None = None, subject: str = "demo-researcher") -> str:
    now = datetime.now(UTC)
    effective_scopes = scopes or DEFAULT_SCOPES
    payload = {
        "iss": DEMO_ISSUER,
        "aud": DEMO_AUDIENCE,
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=1)).timestamp()),
        "scope": " ".join(effective_scopes),
        "scopes": effective_scopes
    }
    return jwt.encode(payload, DEMO_SECRET, algorithm=DEMO_ALGORITHM)


def unauthorized(detail: str = "Authentication is missing or invalid.") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": "unauthorized", "detail": detail},
        headers={"WWW-Authenticate": "Bearer"}
    )


def forbidden(detail: str, missing_scope: str | None = None) -> HTTPException:
    body: dict[str, Any] = {"error": "forbidden", "detail": detail}
    if missing_scope:
        body["missingScope"] = missing_scope
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=body)


def decode_authorization_header(authorization: str | None) -> dict[str, Any]:
    if not authorization:
        audit("auth_failure", reason="missing_authorization")
        raise unauthorized("Missing bearer token.")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        audit("auth_failure", reason="invalid_authorization_scheme")
        raise unauthorized("Expected Authorization: Bearer <token>.")

    try:
        return jwt.decode(
            token,
            DEMO_SECRET,
            algorithms=[DEMO_ALGORITHM],
            audience=DEMO_AUDIENCE,
            issuer=DEMO_ISSUER
        )
    except jwt.PyJWTError as error:
        audit("auth_failure", reason="invalid_token", detail=str(error))
        raise unauthorized("Bearer token could not be verified.") from error


def token_scopes(token: dict[str, Any]) -> set[str]:
    scopes = token.get("scopes")
    if isinstance(scopes, list):
        return {str(scope) for scope in scopes}

    scope_string = token.get("scope", "")
    if isinstance(scope_string, str):
        return set(scope_string.split())

    return set()


def require_token(
    authorization: Annotated[str | None, Header(alias="Authorization")] = None
) -> dict[str, Any]:
    return decode_authorization_header(authorization)


def enforce_scopes(token: dict[str, Any], required_scopes: list[str]) -> None:
    granted_scopes = token_scopes(token)
    for required_scope in required_scopes:
        if required_scope not in granted_scopes:
            audit(
                "auth_failure",
                reason="missing_scope",
                subject=token.get("sub"),
                missing_scope=required_scope,
                granted_scopes=sorted(granted_scopes)
            )
            raise forbidden(f"Missing required scope: {required_scope}.", required_scope)


def require_scopes(required_scopes: list[str]) -> Callable[[str | None], dict[str, Any]]:
    def dependency(
        authorization: Annotated[str | None, Header(alias="Authorization")] = None
    ) -> dict[str, Any]:
        token = decode_authorization_header(authorization)
        enforce_scopes(token, required_scopes)
        return token

    return dependency
