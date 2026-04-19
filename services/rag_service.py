from rag_pipeline import generate_answer

def get_answer(query):
    answer, sources = generate_answer(query)
    return answer, sources
