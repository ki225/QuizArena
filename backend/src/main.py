import asyncio
from fastapi import FastAPI
from src.api.routes import router as api_router
from .db.base import init_db
from .db.session import engine

app = FastAPI()

# 將 api 模組註冊到 app
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    await init_db(engine)