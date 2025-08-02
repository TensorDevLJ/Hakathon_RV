# utils.py (Hugging Face version)
import fitz  # PyMuPDF
import requests
from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()

# Hugging Face Q&A model pipeline
pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")


def extract_text_from_pdf(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        return "Error downloading PDF."

    pdf_file = fitz.open(stream=response.content, filetype="pdf")
    text = ""
    for page in pdf_file:
        text += page.get_text()

    # 👇 Add this line to preview the first 1000 characters of extracted PDF text
    print("\n[DEBUG] Extracted Text (first 1000 characters):\n")
    print(text[:1000])
    print("\n[DEBUG] Total characters extracted:", len(text))

    return text



def ask_gpt(context: str, question: str) -> str:
    try:
        result = qa_pipeline({
            "question": question,
            "context": context
        })

        if result["score"] < 0.2 or result["answer"].strip() == "":
            return "Not mentioned in the document."
        return result["answer"]

    except Exception as e:
        return f"Error: {str(e)}"
