from pypdf import PdfReader
import os

def load_documents(folder):

    docs = []

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if file.endswith(".pdf"):

            reader = PdfReader(path)

            text = ""

            for page in reader.pages:
                text += page.extract_text()

            docs.append({
                "text": text,
                "source": file
            })

        elif file.endswith(".txt"):

            with open(path) as f:
                text = f.read()

            docs.append({
                "text": text,
                "source": file
            })

    return docs

def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i+chunk_size]

        chunks.append(chunk)

    return chunks