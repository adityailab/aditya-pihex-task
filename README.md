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

# 3. Then open
http://localhost:8000/docs
```

---
### Input & Output Screenshot of SwaggerUI
![input](https://github.com/adityailab/aditya-pihex-task/blob/main/Screenshot%202025-08-04%20at%205.53.53%E2%80%AFPM.png)
![Output](https://github.com/adityailab/aditya-pihex-task/blob/main/Screenshot%202025-08-04%20at%205.55.22%E2%80%AFPM.png)
## 📥 API Usage

**Endpoint:** `POST /ask`  
**Body:**

```json
{
  "question": "We need data residency in India. Is that available?"
}
```

**Response:**
```json
{
  "answer": "Yes, data residency in India (India region) is available according to the provided documentation.",
  "category": "security",
  "confidence": 0.9,
  "sources": [
    {
      "doc": "policy_security.md",
      "snippet": "Regional data residency: in (India) and eu (Frankfurt) regions."
    },
    {
      "doc": "changelog.md",
      "snippet": "India (in) region generally available."
    }
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
