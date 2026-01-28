from typing import List

import fasttext
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware  # 引入 CORS中间件模块

# 设置允许访问的域名
origins = ["*"]  # "*"，即为所有。

app = FastAPI(title="FastText Language Detection Service", version="1.0", docs_url=None)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"],
)  # 允许跨域的headers，可以用来鉴别来源等作用。
# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")


# 使用本地的 Swagger UI 静态资源
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Custom Swagger UI",
        swagger_js_url="/static/swagger-ui/5.9.0/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/5.9.0/swagger-ui.css",
    )


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset=utf-8>
            <title>Api information</title>
        </head>
        <body>
            <a href='./docs'>Documents of API</a>
        </body>
    </html>
    """


@app.get("/test")
async def test():
    """
    测试接口，用于验证服务是否正常运行。
    """
    return PlainTextResponse("success")


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
