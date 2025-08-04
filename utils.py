import os
import markdown
from pathlib import Path

def load_markdown_files(folder):
    docs = []
    for file in Path(folder).glob("*.md"):
        text = Path(file).read_text(encoding="utf-8")
        clean_text = markdown.markdown(text)  # Convert to HTML-like, strip if needed
        docs.append({"doc": file.name, "text": clean_text})
    return docs

def chunk_text(text, max_tokens=150):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunk = " ".join(words[i:i + max_tokens])
        chunks.append(chunk)
    return chunks
