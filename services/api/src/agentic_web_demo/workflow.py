import hashlib
from typing import Any

from fastapi import HTTPException, status

from .audit import audit
from .corpus import document_by_id
from .models import CreateReviewDraftRequest


def create_draft(payload: CreateReviewDraftRequest, origin: str) -> dict[str, Any]:
    missing_ids = [
        document_id for document_id in payload.source_document_ids if not document_by_id(document_id)
    ]
    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_source_documents", "detail": f"Unknown document IDs: {', '.join(missing_ids)}"}
        )

    digest = hashlib.sha256(
        "|".join([payload.topic, *payload.source_document_ids, *payload.outline]).encode("utf-8")
    ).hexdigest()[:12]
    draft = {
        "draftId": f"draft-{digest}",
        "status": "pending_review" if payload.human_review_required else "draft",
        "reviewUrl": f"{origin}/reviews/drafts/draft-{digest}"
    }
    audit(
        "review_draft_created",
        draft_id=draft["draftId"],
        source_document_ids=payload.source_document_ids,
        human_review_required=payload.human_review_required
    )
    return draft


def outline_from_results(question: str, results: list[dict[str, Any]]) -> list[str]:
    if not results:
        return [f"Frame the research question: {question}", "Identify primary protocols.", "Compare tradeoffs."]

    protocol_titles = ", ".join(result["title"] for result in results[:3])
    return [
        f"Frame the research question around: {question}",
        f"Compare interoperability approaches using {protocol_titles}.",
        "Separate discovery, delegated identity, tool access, and agent-to-agent delegation.",
        "Require human review before publishing or sharing the draft."
    ]
