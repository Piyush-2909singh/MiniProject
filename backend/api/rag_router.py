from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
from rag import engine
from auth import security
from database import models
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

router = APIRouter()

class AskRequest(BaseModel):
    question: str

class SourceInfo(BaseModel):
    document: str
    chunk_id: int
    score: float

class AskResponse(BaseModel):
    answer: str
    sources: List[SourceInfo]

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest, authorization: str | None = Header(None), x_api_key: str | None = Header(None)):
    # 1. Retrieve context
    results = engine.query_db(request.question, top_k=3)
    
    context_texts = []
    sources = []
    
    if results:
        for doc, score in results:
            context_texts.append(doc.page_content)
            sources.append(SourceInfo(
                document=doc.metadata.get("document_name", "Unknown"),
                chunk_id=doc.metadata.get("chunk_id", 0),
                score=score
            ))
        
    context = "\n\n---\n\n".join(context_texts) if context_texts else "No document context available."
    
    # 2. Get API key from environment, or from the client request as a backup
    import os
    gemini_key = os.getenv("GEMINI_API_KEY", x_api_key)
    
    if not gemini_key:
        return AskResponse(
            answer="Error: No Gemini API Key provided. Please tap the settings icon in the chat to enter your free Gemini API Key.", 
            sources=sources
        )
        
    # 3. Generate Answer using Gemini API (Offloading compute)
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=gemini_key,
            temperature=0.3,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        messages = [
            SystemMessage(content="You are an intelligent enterprise knowledge assistant. If the user asks a greeting or casual question (like 'hello' or 'how are you?'), respond naturally and politely. For any other questions, answer them concisely and accurately ONLY using the provided context. If the answer is not contained in the context and it is not a casual greeting, explicitly state 'I do not have enough context in the uploaded documents to answer this.' Do not hallucinate."),
            HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{request.question}")
        ]
        
        response = llm.invoke(messages)
        answer = str(response.content).strip()
    except Exception as e:
        answer = f"Error during Cloud LLM generation: {str(e)}"
        
    return AskResponse(answer=answer, sources=sources)
