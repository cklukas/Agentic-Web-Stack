import json
import re
from functools import lru_cache
from typing import Any

from .audit import audit
from .paths import DATA_DIR

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "expose access tokens",
    "reveal secrets",
    "bypass tool policy"
]


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


@lru_cache
def load_documents() -> list[dict[str, Any]]:
    return json.loads((DATA_DIR / "corpus.json").read_text(encoding="utf-8"))


def document_by_id(document_id: str) -> dict[str, Any] | None:
    return next((doc for doc in load_documents() if doc["documentId"] == document_id), None)


def public_document(document: dict[str, Any]) -> dict[str, Any]:
    return {
        "documentId": document["documentId"],
        "title": document["title"],
        "sourceUrl": document["sourceUrl"],
        "authors": document.get("authors", []),
        "publishedYear": document.get("publishedYear"),
        "visibility": document.get("visibility", "public")
    }


def detect_prompt_injection(text: str) -> bool:
    normalized = text.lower()
    return any(pattern in normalized for pattern in PROMPT_INJECTION_PATTERNS)


def best_snippet(document: dict[str, Any], query_tokens: list[str]) -> str:
    excerpts = document.get("excerpts", [])
    if not excerpts:
        return document.get("abstract", "")

    def excerpt_score(excerpt: str) -> int:
        haystack = set(tokenize(excerpt))
        return sum(1 for token in query_tokens if token in haystack)

    return max(excerpts, key=excerpt_score)


def search_documents(query: str, year_from: int | None = None, limit: int = 5) -> list[dict[str, Any]]:
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    results: list[dict[str, Any]] = []
    for document in load_documents():
        published_year = document.get("publishedYear")
        if year_from and published_year and published_year < year_from:
            continue

        haystack = " ".join(
            [
                document.get("title", ""),
                document.get("abstract", ""),
                " ".join(document.get("keywords", [])),
                " ".join(document.get("excerpts", []))
            ]
        ).lower()
        matched_terms = sum(1 for token in query_tokens if token in haystack)
        if matched_terms == 0:
            continue

        snippet = best_snippet(document, query_tokens)
        if detect_prompt_injection(snippet):
            audit(
                "prompt_injection_detected",
                document_id=document["documentId"],
                secretDisclosure=False,
                toolPolicyBypassed=False
            )

        score = round(min(1.0, 0.35 + (matched_terms / (len(query_tokens) + 2))), 3)
        results.append(
            {
                "documentId": document["documentId"],
                "title": document["title"],
                "snippet": snippet,
                "sourceUrl": document["sourceUrl"],
                "score": score,
                "_publishedYear": published_year or 0
            }
        )

    results.sort(key=lambda item: (item["score"], item["_publishedYear"], item["title"]), reverse=True)
    return [{key: value for key, value in result.items() if not key.startswith("_")} for result in results[:limit]]


def expand_related_documents(document_ids: list[str]) -> list[str]:
    related: list[str] = []
    for document_id in document_ids:
        document = document_by_id(document_id)
        if not document:
            continue
        for related_id in document.get("relatedDocumentIds", []):
            if related_id not in related and related_id not in document_ids:
                related.append(related_id)
    return related


def approved_excerpts(document: dict[str, Any]) -> list[str]:
    return [excerpt for excerpt in document.get("excerpts", []) if not detect_prompt_injection(excerpt)]
