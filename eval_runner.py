import json
import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# Load schema
with open("answer_schema.json") as f:
    answer_schema = json.load(f)

# Load test queries
with open("eval_questions.jsonl") as f:
    questions = [json.loads(line) for line in f.readlines()]

print(f"Loaded {len(questions)} questions from eval_questions.jsonl")

# API endpoint
API_URL = "http://localhost:8000/ask"

passed = 0
failed = 0

for idx, q in enumerate(questions):
    question_text = q.get("question")
    expected_category = q.get("expected_category")
    expected_contains = q.get("expected_contains", [])

    try:
        response = requests.post(API_URL, json={"question": question_text})
        response.raise_for_status()
        data = response.json()

        # Validate schema
        validate(instance=data, schema=answer_schema)

        print(f"\n✅ Q{idx+1}: {question_text}")
        print(f"→ Answer: {data['answer']}")
        print(f"→ Category: {data['category']}")
        print(f"→ Confidence: {data['confidence']}")
        print(f"→ Sources: {[s['doc'] for s in data.get('sources', [])]}")

        # Optional: soft match checks
        if expected_category and data['category'] != expected_category:
            print(f"⚠️ Expected category: {expected_category}, but got: {data['category']}")

        if expected_contains:
            if not any(keyword.lower() in data['answer'].lower() for keyword in expected_contains):
                print(f"⚠️ Expected answer to include one of: {expected_contains}")
        
        passed += 1

    except (requests.RequestException, ValidationError, KeyError) as e:
        print(f"\n❌ Q{idx+1} failed: {question_text}")
        print(f"Error: {e}")
        failed += 1

print(f"\n---\n✅ Passed: {passed}, ❌ Failed: {failed}, Total: {len(questions)}")
