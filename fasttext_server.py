from fastapi import FastAPI
from pydantic import BaseModel
import fasttext
from typing import List

app = FastAPI(title="FastText Language Detection Service", version="1.0")

# 模型只加载一次
MODEL_PATH = "./models/lid.176.bin"
model = fasttext.load_model(MODEL_PATH)


# 请求 / 响应模型
class PredictRequest(BaseModel):
    texts: List[str]
    top_k: int = 1


class PredictItem(BaseModel):
    label: str
    prob: float


@app.post("/predict", response_model=List[List[PredictItem]])
def predict(req: PredictRequest):
    results = []

    for text in req.texts:
        labels, probs = model.predict(text, k=req.top_k)
        items = [
            {"label": label.replace("__label__", ""), "prob": float(prob)}
            for label, prob in zip(labels, probs)
        ]
        results.append(items)

    return results


@app.get("/health")
def health():
    return {"status": "ok"}
