from ollama import Client

# Use Docker-aware host
client = Client(host="http://host.docker.internal:11434")  # macOS/Windows


def generate_answer(question, chunks):
    context = "\n\n".join([c["text"] for c in chunks])

    
    prompt = f"""You are a strict documentation assistant. You must only use the information provided below.

DOCUMENTATION:
{context}

QUESTION:
{question}

If you cannot find the answer in the documentation, respond with:
"I'm not sure based on the documentation."

You are not allowed to guess or assume anything.

Strictly based on the documentation above, what is the answer?
"""


    response = client.chat(model='mistral', messages=[
        {"role": "user", "content": prompt}
    ])

    return response['message']['content'].strip()
