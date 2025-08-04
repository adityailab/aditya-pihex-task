import difflib

def guess_category_by_content(answer: str, sources: list[dict]) -> str:
    doc_to_category = {
        "policy_security.md": "security",
        "policy_api.md": "api",
        "policy_pricing.md": "pricing",
        "product_quickstart.md": "quickstart",
        "support_faq.md": "support",
        "troubleshooting.md": "troubleshooting",
        "changelog.md": "changelog",
    }

    # Score each doc based on content overlap
    category_scores = {}

    for src in sources:
        doc = src.get("doc")
        snippet = src.get("snippet", "")
        category = doc_to_category.get(doc, "other")

        # Compute similarity score between snippet and final answer
        score = difflib.SequenceMatcher(None, snippet.lower(), answer.lower()).ratio()
        category_scores[category] = category_scores.get(category, 0) + score

    # Pick the highest scoring category
    if category_scores:
        best_category = max(category_scores, key=category_scores.get)
        return best_category

    return "other"

def estimate_confidence(answer: str, num_chunks: int) -> float:
    """
    Estimate confidence based on retrieved content and answer quality.
    """
    if "not sure based on the documentation" in answer.lower():
        return 0.3  # low confidence if answer says it doesn't know

    base = 0.6
    increment = 0.1 * min(num_chunks, 3)
    return round(min(1.0, base + increment), 2)
