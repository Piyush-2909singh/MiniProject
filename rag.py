import fitz

def read_pdf(path):
    doc = fitz.open(path)
    text = ""

    for page in doc:
        text = text + page.get_text()

    return text