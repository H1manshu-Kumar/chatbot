# minimal_main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io

app = FastAPI()

df = None
vectorizer = None
tfidf_matrix = None

def build_index_from_df(dataframe, text_col):
    global df, vectorizer, tfidf_matrix
    df = dataframe.copy()
    corpus = df[text_col].astype(str).tolist()
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)

@app.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...), text_column: str = None):
    contents = await file.read()
    df_local = pd.read_excel(io.BytesIO(contents))
    if text_column and text_column in df_local.columns:
        text_col = text_column
    else:
        df_local['content'] = df_local.astype(str).agg(' '.join, axis=1)
        text_col = 'content'
    build_index_from_df(df_local, text_col)
    return {"status":"ok","rows":len(df_local), "text_column": text_col}

class ChatRequest(BaseModel):
    message: str
    top_k: int = 3

@app.post("/chat")
def chat(req: ChatRequest):
    if tfidf_matrix is None:
        return {"error":"No data loaded. Upload Excel via /upload_excel"}
    q_vec = vectorizer.transform([req.message])
    sims = cosine_similarity(q_vec, tfidf_matrix).flatten()
    topk_idx = sims.argsort()[::-1][:req.top_k]
    answers = []
    for idx in topk_idx:
        row = df.iloc[idx].to_dict()
        if 'answer' in df.columns:
            answer_text = str(df.iloc[idx]['answer'])
        else:
            answer_text = ' | '.join([f"{k}:{v}" for k,v in row.items()])
        answers.append({"answer": answer_text, "score": float(sims[idx]), "row": row})
    return {"answers": answers}
