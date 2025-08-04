from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from utils import chunk_text

class Retriever:
    def __init__(self, docs):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)  # dimension of embedding
        self.chunks = []

        embeddings = []
        for doc in docs:
            for chunk in chunk_text(doc['text']):
                emb = self.model.encode(chunk)
                embeddings.append(emb)
                self.chunks.append({
                    "doc": doc['doc'],
                    "text": chunk
                })
        self.index.add(np.array(embeddings).astype("float32"))

    def search(self, query, k=5, min_score=0.5):
        q_emb = self.model.encode(query)
        D, I = self.index.search(np.array([q_emb]).astype("float32"), k)

        results = []
        for score, idx in zip(D[0], I[0]):
            chunk = self.chunks[idx]
            similarity = 1 - (score / 4)  # normalize L2 distance (approx)
            if similarity >= min_score:
                results.append(chunk)

        return results


