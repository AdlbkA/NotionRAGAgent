import uvicorn
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from datetime import datetime
from src.di import setup_http_di
from src.api.read import router as read_router
from ai.rag.retriever import Retriever
from ai.notion.sync import sync_notion_to_rag



container = setup_http_di()
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    retriever = await container.get(Retriever)

    scheduler.add_job(
        sync_notion_to_rag,
        "interval",
        hours=1,
        args=[retriever],
        next_run_time=datetime.now(),
        id="sync_notion_to_rag",
        replace_existing=True,
    )
    scheduler.start()

    yield
    await container.close()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)    

app = FastAPI(title="NotionRAGAgent", lifespan=lifespan)

setup_dishka(container, app)

app.include_router(read_router)

@app.get('/health')
async def health_check():
    return {'status': 'OK'}

if __name__ == '__main__':
    uvicorn.run('src.main:app', host='0.0.0.0', port=8000, reload=True)