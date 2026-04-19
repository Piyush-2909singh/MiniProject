
import os
import re
from search import search
from transformers import pipeline

RELEVANCE_MAX_DISTANCE = 1.45

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)


def generate_answer(question):

    if not has_indexed_documents():
        return "No documents are available yet. Please upload and index documents first.", []

    cleaned_question = (question or "").strip()
    normalized_question = re.sub(r"[^a-zA-Z0-9\s]", " ", cleaned_question).lower().strip()
    tokens = [t for t in normalized_question.split() if t]

    greeting_tokens = {"hi", "hello", "hey", "yo", "hola"}
    if tokens and any(t in greeting_tokens for t in tokens) and len(tokens) <= 6:
        return "Hello! Ask me a question about your uploaded documents.", []

    acronym_map = {
        "os": "operating system",
        "vm": "virtual memory",
        "cpu": "central processing unit"
    }

    expanded_tokens = [acronym_map.get(t, t) for t in tokens]
    search_question = " ".join(expanded_tokens) if expanded_tokens else cleaned_question

    docs = search(
        search_question,
        k=3,
        max_distance=RELEVANCE_MAX_DISTANCE,
        include_distance=True
    )

    if not docs:
        return "I couldn't find relevant information in your uploaded documents.", []

    context = ""

    sources = []
    for d in docs:
        context += d.get("text", "") + "\n"
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

Question: {cleaned_question}

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