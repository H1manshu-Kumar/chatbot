# AI Assistant Prototype

This project provides two prototypes of a chatbot that uses data files as source.

## Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Minimal (no LLM)
```bash
uvicorn minimal_main:app --reload --host 0.0.0.0 --port 8000
```

## Run RAG (embeddings + OpenAI)
```bash
export OPENAI_API_KEY="yourkey"
uvicorn rag_main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend
Open `login.html` in your browser. Upload a data file and start asking questions.

## Example Data
See `example.xlsx` included in project.
