
import os
from search import search
from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

def generate_answer(question):

    docs = search(question)

    if not docs:
        return "No relevant info found", []

    context = ""

    sources = []
    for d in docs:
        context += d["text"] + "\n"
        # Only add the document name (not path)
        src = d.get("source", "Unknown")
        doc_name = os.path.basename(src)
        sources.append(doc_name)
    # Remove duplicates
    sources = list(dict.fromkeys(sources))

    context = context[:800]

    prompt = f"""
Use the context to answer the question.

Context:
{context}

Question: {question}

Answer in one sentence:
"""

    result = generator(
        prompt,
        max_new_tokens=60,
        do_sample=False,
        repetition_penalty=1.5
    )

    text = result[0]["generated_text"]

    answer = text.replace(prompt, "").strip()

    return answer, sources