from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent import chat
from mcp_conf.sync import sync_notion_to_rag

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    return {"response": await chat(req.message)}

@app.post("/sync")
async def sync_endpoint():
    await sync_notion_to_rag()
    return {"status": "ok"}