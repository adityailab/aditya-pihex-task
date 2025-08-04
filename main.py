from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from model import AnswerResponse
from retriever import Retriever
from utils import load_markdown_files
from scoring import guess_category_by_content,estimate_confidence
from validate_schema import validate_answer
from llm import generate_answer  # use your Ollama version now

import difflib
import re

def split_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)

def strip_html_tags(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text)

def get_relevant_sources(answer: str, chunks: list[dict], threshold: float = 0.3) -> list[dict]:
    def strip_html(text):
        return re.sub(r'<[^>]+>', '', text)

    def get_keywords(text):
        return {w for w in re.findall(r'\b\w+\b', text.lower()) if w not in {"the", "and", "or", "is", "to", "in", "of", "on", "for", "at"}}

    seen = set()
    selected = []
    answer_sents = split_sentences(answer)

    for chunk in chunks:
        doc = chunk["doc"]
        chunk_text = strip_html(chunk["text"])
        chunk_sents = split_sentences(chunk_text)

        for a_sent in answer_sents:
            a_keywords = get_keywords(a_sent)
            for c_sent in chunk_sents:
                score = difflib.SequenceMatcher(None, a_sent.lower(), c_sent.lower()).ratio()
                c_keywords = get_keywords(c_sent)
                if score >= threshold and len(a_keywords & c_keywords) >= 3:
                    if doc not in seen:
                        selected.append({
                            "doc": doc,
                            "snippet": c_sent.strip()
                        })
                        seen.add(doc)
                    break  # avoid adding multiple times

    return selected






# -------------------
# Setup
# -------------------
app = FastAPI()

# Load and index knowledge base
docs = load_markdown_files("kb")
retriever = Retriever(docs)

# -------------------
# Request Body
# -------------------
class AskRequest(BaseModel):
    question: str

# -------------------
# Endpoint
# -------------------
@app.post("/ask", response_model=AnswerResponse)
def ask(request: AskRequest):
    question = request.question
    chunks = retriever.search(question, k=3)

    # sources = [
    #     {
    #         "doc": chunk["doc"],
    #         "snippet": chunk["text"][:200]
    #     } for chunk in chunks
    # ]

    answer_text = generate_answer(question, chunks) if chunks else "Sorry, I could not find an answer."
    #  answer_text = generate_answer(question, chunks) if chunks else "Sorry, I could not find an answer."

    # Check if answer is a fallback (i.e. LLM couldn't answer from docs)
    is_unsure = "not sure based on the documentation" in answer_text.lower()

    sources = get_relevant_sources(answer_text, chunks) if not is_unsure else []

    category = guess_category_by_content(answer_text, sources)

# fallback if category is 'other' or no sources found
    if category == "other" and chunks:
        doc_to_category = {
        "policy_security.md": "security",
        "policy_api.md": "api",
        "policy_pricing.md": "pricing",
        "product_quickstart.md": "other",
        "support_faq.md": "support",
        "troubleshooting.md": "other",
        "changelog.md": "other",
         }
        fallback_doc = chunks[0]["doc"]
        category = doc_to_category.get(fallback_doc, "other")


    response = {
    "answer": answer_text,
    "category": guess_category_by_content(answer_text, sources),
    "confidence": estimate_confidence(answer_text, len(chunks)),
    "sources": sources
    }


    try:
        validate_answer(response)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return response

