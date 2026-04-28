
import os
import re
import traceback
from search import search, has_indexed_documents
from transformers import pipeline

RELEVANCE_MAX_DISTANCE = 1.2
MIN_KEYWORD_OVERLAP = 0.2
MIN_KEYWORD_MATCHES = 1

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

def build_snippet(text, max_len=200):
    cleaned = text or ""
    cleaned = re.sub(r"\bPage\s+\d+(\s+of\s+\d+)?\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b\d{1,2}:\d{2}(?::\d{2})?\b", "", cleaned)
    cleaned = re.sub(r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b", "", cleaned)
    cleaned = re.sub(r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b", "", cleaned)
    cleaned = re.sub(r"\b\d{5,}\b", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if not cleaned:
        cleaned = re.sub(r"\s+", " ", (text or "")).strip()

    sentences = [s for s in re.split(r"(?<=[.!?])\s+", cleaned) if s]
    snippet = " ".join(sentences[:2]).strip()
    if not snippet:
        snippet = cleaned
    if len(snippet) > max_len:
        snippet = snippet[:max_len].rsplit(" ", 1)[0].strip() or snippet[:max_len].strip()
    return snippet

def build_fallback_answer(context, max_len=400):
    cleaned = re.sub(r"\s+", " ", (context or "")).strip()
    if not cleaned:
        return (
            "I found relevant information, but could not generate a complete answer. "
            "Please refer to the sources below."
        )
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", cleaned) if s]
    snippet = " ".join(sentences[:2]).strip() or cleaned
    if len(snippet) > max_len:
        snippet = snippet[:max_len].rsplit(" ", 1)[0].strip() or snippet[:max_len].strip()
    return snippet

def keyword_overlap_score(query_tokens, text):
    if not query_tokens:
        return 0.0, 0
    normalized = re.sub(r"[^a-zA-Z0-9\s]", " ", text or "").lower()
    text_tokens = {t for t in normalized.split() if t}
    matches = sum(1 for t in query_tokens if t in text_tokens)
    return matches / max(len(query_tokens), 1), matches
def generate_answer(question):
    sources = []
    try:
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
        filtered_docs = []
        for d in docs:
            chunk_text = d.get("text", "") or ""
            overlap_ratio, overlap_matches = keyword_overlap_score(tokens, chunk_text)
            if overlap_matches < MIN_KEYWORD_MATCHES or overlap_ratio < MIN_KEYWORD_OVERLAP:
                continue
            filtered_docs.append(d)

        if not filtered_docs:
            return "I couldn't find relevant information in your uploaded documents.", []

        context = ""
        sources = []
        sources_map = {}
        for d in filtered_docs:
            chunk_text = d.get("text", "") or ""
            context += chunk_text + "\n"

            document = d.get("document")
            if not document:
                src = d.get("source", "Unknown")
                document = os.path.basename(src)

            snippet = build_snippet(chunk_text)
            entry = sources_map.get(document)
            if entry is None:
                entry = {"document": document, "snippets": []}
                sources_map[document] = entry
                sources.append(entry)
            if snippet and snippet not in entry["snippets"]:
                entry["snippets"].append(snippet)
            if len(entry["snippets"]) >= 2:
                entry["snippets"] = entry["snippets"][:2]
            if len(sources) >= 3:
                break

        context = context[:800]

        is_definition_question = "what is" in cleaned_question.lower()
        if is_definition_question:
            instruction = (
                "Using ONLY the provided context, extract or minimally rephrase a clear definition to answer the question. "
                "Do not introduce new concepts or wording not present in the context. "
                "Keep the answer to 1–2 sentences."
            )
        else:
            instruction = (
                "Using ONLY the provided context, extract or minimally rephrase a clear answer. "
                "If definition-like content exists, use it directly. "
                "Do not introduce new concepts or wording not present in the context. "
                "Keep the answer to 1–2 sentences."
            )

        prompt = f"""
Use the context to answer the question.

Context:
{context}

Question: {cleaned_question}

{instruction}
Answer ONLY using the provided context. If context is insufficient, say you don't know.
Answer:
"""

        result = generator(
            prompt,
            max_new_tokens=60,
            do_sample=False,
            repetition_penalty=1.5
        )

        text = result[0]["generated_text"]
        answer = text.replace(prompt, "").strip()
        if not answer:
            answer = build_fallback_answer(context)
        if not answer:
            answer = (
                "I found relevant information, but could not generate a complete answer. "
                "Please refer to the sources below."
            )
        print("Generated Answer:", answer)
        return answer, sources
    except Exception as e:
        print("RAG Pipeline Error:", e)
        print(traceback.format_exc())
        fallback = build_fallback_answer(context) if 'context' in locals() else (
            "I found relevant information, but could not generate a complete answer. "
            "Please refer to the sources below."
        )
        return fallback, sources