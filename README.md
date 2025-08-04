# 📘 PiHex Structured Answering API

This FastAPI-based service answers questions based on a Markdown knowledge base and returns structured responses conforming to a strict JSON schema.

## 🚀 Features

- ✅ Embedding-based document retrieval
- 🧠 Answer generation using a local LLM (via Ollama)
- 📂 Markdown knowledge base ingestion
- ✅ Strict schema validation (answer, category, confidence, sources)
- 🐳 Docker support

---

## 📦 Requirements

- Python 3.12+
- [Ollama](https://ollama.com/) with a local LLM (e.g. `mistral`)
- pip / virtualenv / Docker (optional)

---

## 🧪 Local Setup

```bash
# 1. Clone repo & navigate in
git clone <your-repo-url>
cd pihex-task

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
uvicorn main:app --reload
```

Visit the interactive API at:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Run with Docker

```bash
# 1. Build the image
docker build -t pihex-api .

# 2. Run the container
docker run -p 8000:8000 pihex-api
```

---

## 📥 API Usage

**Endpoint:** `POST /ask`  
**Body:**

```json
{
  "question": "How does PiHex handle PII?"
}
```

**Response:**
```json
{
  "answer": "...",
  "category": "...",
  "confidence": 0.9,
  "sources": [
    { "doc": "...", "snippet": "..." }
  ]
}
```

---

## 🧪 Evaluation

```bash
python eval_runner.py
```

Runs questions from `eval_questions.jsonl` and compares output to expected criteria.

---