from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = None
vectorizer = None
tfidf_matrix = None

@app.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...)):
    global df, vectorizer, tfidf_matrix
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))
    df['content'] = df.astype(str).agg(' '.join, axis=1)
    
    corpus = df['content'].tolist()
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    return {"status": "ok", "rows": len(df), "columns": list(df.columns)}

class ChatRequest(BaseModel):
    message: str
    top_k: int = 3

@app.post("/chat")
def chat(req: ChatRequest):
    if tfidf_matrix is None:
        return {"error": "No data loaded. Upload Excel first."}
    
    q_vec = vectorizer.transform([req.message])
    sims = cosine_similarity(q_vec, tfidf_matrix).flatten()
    topk_idx = sims.argsort()[::-1][:req.top_k]
    
    answers = []
    for idx in topk_idx:
        if sims[idx] > 0:
            row_data = df.iloc[idx].to_dict()
            answer_text = ' | '.join([f"{k}: {v}" for k, v in row_data.items() if k != 'content'])
            answers.append({"answer": answer_text, "score": float(sims[idx])})
    
    return {"answers": answers}
