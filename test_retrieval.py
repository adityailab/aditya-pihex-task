from utils import load_markdown_files
from retriever import Retriever

docs = load_markdown_files("kb")
retriever = Retriever(docs)

query = "How do I authenticate with the PiHex API?"
results = retriever.search(query, k=1)

for i, r in enumerate(results):
    print(f"\nResult {i+1}")
    print(f"[{r['doc']}] {r['text'][:200ae]}...")
