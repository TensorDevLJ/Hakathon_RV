# main.py
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from utils import extract_text_from_pdf, ask_gpt
import os
import time
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

TEAM_TOKEN = os.getenv("TEAM_TOKEN")

class QueryRequest(BaseModel):
    documents: str
    questions: list[str]

class QueryResponse(BaseModel):
    answers: list[str]

@app.post("/hackrx/run", response_model=QueryResponse)
async def run_webhook(data: QueryRequest, authorization: str = Header(...)):
    try:
        if authorization != f"Bearer {TEAM_TOKEN}":
            raise HTTPException(status_code=401, detail="Invalid Bearer token")

        start = time.time()
        text = extract_text_from_pdf(data.documents)
        print("✅ PDF extracted in:", round(time.time() - start, 2), "seconds")

        answers = []
        for q in data.questions:
            q_start = time.time()
            answer = ask_gpt(text, q)
            print(f"✅ Answered: '{q}' in {round(time.time() - q_start, 2)} seconds")
            answers.append(answer)

        return {"answers": answers}

    except Exception as e:
        print("❌ Internal server error:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
