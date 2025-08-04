import json
from jsonschema import validate, Draft202012Validator

with open("answer_schema.json") as f:
    schema = json.load(f)
    validator = Draft202012Validator(schema)

def validate_answer(response: dict):
    errors = sorted(validator.iter_errors(response), key=lambda e: e.path)
    if errors:
        raise ValueError(f"Schema validation error: {[e.message for e in errors]}")
