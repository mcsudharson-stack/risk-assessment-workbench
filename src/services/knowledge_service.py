from pathlib import Path


KNOWLEDGE_BASE_PATH = Path("data/knowledge_base")


def retrieve_policy_context(change_request):
    query_terms = [
        change_request.change_type.lower(),
        change_request.geography.lower(),
        change_request.customer_segment.lower(),
    ]

    if change_request.vendor_involved:
        query_terms.append("vendor")

    documents = []

    for file_path in KNOWLEDGE_BASE_PATH.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        score = sum(
            1
            for term in query_terms
            if term in content.lower()
        )

        documents.append(
            {
                "source": file_path.name,
                "content": content,
                "score": score,
            }
        )

    documents.sort(
        key=lambda document: document["score"],
        reverse=True,
    )

    return documents[:3]