import datetime
import os
import traceback
from typing import List

import fasttext
from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware  # 引入 CORS中间件模块


def log_error(exception: Exception, log_dir="error"):
    """
    记录错误信息到指定目录，并按日期小时命名文件。

    :param exception: 捕获的异常对象
    :param log_dir: 错误日志存储的目录，默认为 'error'
    """
    # 确保日志目录存在
    os.makedirs(log_dir, exist_ok=True)
    # 获取当前日期和小时，作为日志文件名的一部分
    timestamp_hour = datetime.datetime.now().strftime("%Y-%m-%d_%H")  # 到小时
    # 获取当前时间戳，格式化为 YYYY-MM-DD_HH-MM-SS
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # 创建日志文件路径
    log_file_path = os.path.join(log_dir, f"error_{timestamp_hour}.log")
    # 错误信息
    error_msg = str(exception)
    # 使用 traceback 模块获取详细的错误信息
    error_traceback = traceback.format_exc()
    # 写入错误信息到文件，使用追加模式 'a'
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"timestamp: {timestamp}\n")
        log_file.write(f"exception: {error_msg}\n")
        log_file.write("traceback:\n")
        log_file.write(error_traceback + "\n")


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
    try:
        results = []

        for text in req.texts:
            labels, probs = model.predict(text, k=req.top_k)
            items = [
                {"label": label.replace("__label__", ""), "prob": float(prob)}
                for label, prob in zip(labels, probs)
            ]
            results.append(items)

        return results
    except Exception as e:
        # 记录日志
        log_error(e)
        # 返回 HTTP 500
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
