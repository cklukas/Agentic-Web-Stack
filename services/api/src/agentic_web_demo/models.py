from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class DemoModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class HealthResponse(DemoModel):
    status: Literal["ok"]
    service: str
    version: str


class DevTokenResponse(DemoModel):
    access_token: str
    token_type: Literal["bearer"]
    expires_in: int
    scope: str


class DocumentSearchRequest(DemoModel):
    query: str = Field(min_length=1)
    year_from: int | None = Field(default=None, alias="yearFrom", ge=1900, le=2100)
    limit: int = Field(default=5, ge=1, le=10)


class DocumentPassage(DemoModel):
    document_id: str = Field(alias="documentId")
    title: str
    snippet: str
    source_url: str = Field(alias="sourceUrl")
    score: float | None = None


class DocumentSearchResponse(DemoModel):
    results: list[DocumentPassage]


class DocumentResponse(DemoModel):
    document_id: str = Field(alias="documentId")
    title: str
    source_url: str = Field(alias="sourceUrl")
    authors: list[str] = []
    published_year: int | None = Field(default=None, alias="publishedYear")
    visibility: str


class CreateReviewDraftRequest(DemoModel):
    topic: str = Field(min_length=1)
    source_document_ids: list[str] = Field(alias="sourceDocumentIds", min_length=1)
    outline: list[str] = Field(min_length=1)
    human_review_required: bool = Field(default=True, alias="humanReviewRequired")


class ReviewDraft(DemoModel):
    draft_id: str = Field(alias="draftId")
    status: Literal["draft", "pending_review", "approved", "rejected"]
    review_url: str = Field(alias="reviewUrl")


class RuntimeDebugResponse(DemoModel):
    service: str
    version: str
    corpus_count: int = Field(alias="corpusCount")
    supported_scopes: list[str] = Field(alias="supportedScopes")
    specs: dict[str, Any]


class AuditEvent(BaseModel):
    model_config = ConfigDict(extra="allow")

    timestamp: str
    event: str
    trace_id: str = Field(alias="traceId")


class AuditEventsResponse(DemoModel):
    events: list[AuditEvent]


class TraceEvent(DemoModel):
    timestamp: str
    trace_id: str = Field(alias="traceId")
    event: str
    layer: str
    component: str
    policy_result: str = Field(alias="policyResult")
    artifact_refs: list[str] = Field(default_factory=list, alias="artifactRefs")


class TraceResponse(DemoModel):
    trace_id: str = Field(alias="traceId")
    events: list[TraceEvent]
