from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from database import models
from api import auth_router, document_router, rag_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Knowledge Intelligence Platform", version="1.0.0")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(document_router.router, prefix="/api/docs", tags=["documents"])
app.include_router(rag_router.router, prefix="/api/rag", tags=["rag"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Enterprise Knowledge Intelligence Platform API"}
