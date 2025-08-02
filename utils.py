import fitz  # PyMuPDF
import requests
import re
from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()

# Load QA pipeline (high-quality model)
#qa_pipeline = pipeline("question-answering", model="deepset/roberta-large-squad2")
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")


# Clean and normalize PDF text
def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Extract PDF text from URL
def extract_text_from_pdf(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        return "Error downloading PDF."

    pdf_file = fitz.open(stream=response.content, filetype="pdf")
    text = ""
    for page in pdf_file:
        text += page.get_text()
    return clean_text(text)

# Ask Q&A pipeline with context chunking
def ask_gpt(context: str, question: str) -> str:
    max_chunk = 450
    stride = 50
    chunks = [context[i:i + max_chunk] for i in range(0, len(context), max_chunk - stride)]

    best_answer = ""
    best_score = 0

    for chunk in chunks:
        try:
            result = qa_pipeline(question=question, context=chunk)
    
            if result["score"] > best_score and result["answer"].strip() != "":
                best_answer = result["answer"]
                best_score = result["score"]
        except Exception as e:
            continue

    return best_answer if best_answer else "Not mentioned in the document."
