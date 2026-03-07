FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for unstructured and chroma
RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic-dev \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download HF model to avoid downloading on each start
ENV HF_HUB_DISABLE_SYMLINKS_WARNING=1
RUN python -c "from transformers import pipeline; pipeline('text-generation', model='TinyLlama/TinyLlama-1.1B-Chat-v1.0')" || true

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
