
# 📄 HackRx PDF Q&A API

A FastAPI-based project that takes a list of insurance policy PDF URLs and answers user questions using a powerful transformer-based model (`deepset/roberta-large-squad2`).

## 🚀 Features

- 🔐 Token-based Authentication
- 📄 Multi-PDF support
- 🤖 Transformer-based QA (`transformers` + `PyMuPDF`)
- 💬 Context-aware question answering
- ⚡ Ngrok tunneling support for public access

## 🔧 Tech Stack

- FastAPI
- Uvicorn
- Transformers (Hugging Face)
- PyMuPDF
- Pydantic
- Ngrok (for testing public API)

## 🛠️ Setup Instructions

### 1. ✅ Clone the repo

```bash
git clone https://github.com/your-username/hackrx_fastapi.git
cd hackrx_fastapi
```

### 2. 🐍 Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# OR
source venv/bin/activate   # On Mac/Linux
```

### 3. 📦 Install dependencies

```bash
pip install -r requirements.txt
```

If `torch` fails to install, manually install a compatible CPU version:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 4. 🔑 Set environment variables

Create a `.env` file:

```env
TEAM_TOKEN=your_secret_token_here
```

### 5. ▶️ Run the FastAPI server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. 🌐 Expose using ngrok (for external testing)

```bash
ngrok http 8000
```

It will give you a public URL like:  
`https://abc1234.ngrok-free.app`

## 📬 API Usage (POST `/hackrx/run`)

### ✅ Request Headers

```
Authorization: Bearer your_secret_token_here
Content-Type: application/json
```

### ✅ Request Body

```json
{
  "documents": [
    "https://your-publicly-accessible-pdf-url.pdf"
  ],
  "questions": [
    "What is the waiting period?",
    "Is dental coverage included?",
    "How can I file a claim?"
  ]
}
```

### ✅ Sample Response

```json
{
  "answers": [
    "30 days waiting period for all illnesses except accident.",
    "Dental coverage is excluded unless medically necessary.",
    "Claims can be submitted online or via toll-free number."
  ]
}
```

## ❗Troubleshooting

- If you get a **403 or 409** error on PDF URL:  
  ➤ Make sure the PDF link is **publicly accessible** and has not expired.

- If Postman says: `OPENSSL_internal:BAD_DECRYPT`  
  ➤ Try changing region or use `curl`, or update Postman.

- If model loading takes time, it's normal on **first run**.

## 📁 Files Overview

| File        | Description                        |
|-------------|------------------------------------|
| `main.py`   | FastAPI app and endpoint logic     |
| `utils.py`  | PDF reading and QA logic           |
| `.env`      | Secrets like Bearer token          |
| `requirements.txt` | All required packages       |

## 📞 Support

For issues or questions, please raise an issue or contact the author.
