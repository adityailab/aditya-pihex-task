# 📌 Architecture & Design Notes

## 🏗️ Architecture Overview

The project is a lightweight, containerized FastAPI service that answers user queries based on a small Markdown knowledge base. It uses retrieval-augmented generation (RAG) to generate responses constrained to available documents.

### 🔧 Key Components

1. **FastAPI App (`main.py`)**
   - Exposes a `POST /ask` endpoint.
   - Routes user input through the retrieval, generation, scoring, and schema validation pipeline.

2. **Retriever (`retriever.py`)**
   - Performs basic semantic search over pre-loaded Markdown content.
   - Returns top-k relevant chunks for answering the query.

3. **LLM Answer Generation (`llm.py`)**
   - Uses a locally running Ollama model (e.g., Mistral) to generate the final answer based on retrieved chunks.

4. **Scoring (`scoring.py`)**
   - Estimates answer confidence.
   - Predicts category using snippet-answer similarity with `difflib`.

5. **Schema Validation (`validate_schema.py`)**
   - Ensures strict adherence to the provided `answer_schema.json`.

6. **Evaluation (`eval_runner.py`)**
   - Loads `eval_questions.jsonl` and checks predictions against expected outputs.

---

## ⚖️ Design Trade-offs

### ✅ Simplicity vs. Robustness
- **Pros:** Code is modular and readable, using plain Python and minimal dependencies.
- **Cons:** No vector DB or advanced embeddings; basic scoring may miss nuanced intent.

### 🧠 LLM Usage
- **Choice:** Ollama (Mistral) for local LLM inference avoids latency and cost of cloud APIs.
- **Limitation:** Mistral may hallucinate or deviate from source if not tightly prompted.

### 📄 Retrieval
- **Choice:** Simple scoring based on token overlap + difflib similarity.
- **Limitation:** May miss matches with different phrasing.

### 📁 Source Attribution
- **Strategy:** Return only sources that have overlapping keywords and high sentence similarity.
- **Edge Case:** Short answers may not match chunk length expectations.

---

## 📦 Containerization
- A lightweight Dockerfile ensures the app runs predictably in any environment.
- Only essential system and Python dependencies are included.

---

## 🔍 Improvements (If more time allowed)
- Fine-tuned prompt for better LLM faithfulness.
- Add async support and batch endpoint.
- API key or basic auth protection.
