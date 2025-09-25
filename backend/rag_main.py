# rag_main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd, io, os
from sentence_transformers import SentenceTransformer
import faiss, numpy as np
import openai

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')
index = None
docs = []

def chunk_text(text, max_chars=500):
    sentences = text.split('. ')
    chunks, cur = [], ''
    for s in sentences:
        if len(cur) + len(s) + 1 <= max_chars:
            cur = (cur + ' ' + s).strip()
        else:
            if cur:
                chunks.append(cur)
            cur = s
    if cur:
        chunks.append(cur)
    return chunks

@app.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...), text_column: str = None):
    global index, docs
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))
    if text_column and text_column in df.columns:
        df['content'] = df[text_column].astype(str)
    else:
        df['content'] = df.astype(str).agg(' '.join, axis=1)
    docs = []
    for _, row in df.iterrows():
        for c in chunk_text(str(row['content'])):
            docs.append({"text": c, "meta": row.to_dict()})
    embeddings = model.encode([d['text'] for d in docs], convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return {"status":"ok", "chunks": len(docs)}

class ChatRequest(BaseModel):
    message: str
    top_k: int = 3

@app.post("/chat")
def chat(req: ChatRequest):
    if index is None:
        return {"error":"No index loaded. Upload Excel first."}
    q_emb = model.encode([req.message], convert_to_numpy=True)
    D, I = index.search(q_emb, req.top_k)
    hits = []
    for idx, dist in zip(I[0], D[0]):
        hits.append({"text": docs[idx]['text'], "meta": docs[idx]['meta'], "score": float(dist)})
    context = "\n\n".join([f"Source {i+1}: {h['text']}" for i,h in enumerate(hits)])
    prompt = f\"Use this context to answer: {context}\n\nQuestion: {req.message}\"
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error":"OPENAI_API_KEY not set. Sources returned.", "sources": hits}
    openai.api_key = api_key
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are a helpful assistant."},
            {"role":"user","content":prompt}
        ],
        max_tokens=400,
        temperature=0.0,
    )
    answer = resp['choices'][0]['message']['content']
    return {"answer": answer, "sources": hits}
