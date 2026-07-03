from fastapi import APIRouter
from pydantic import BaseModel
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from ai.notion.sync import sync_notion_to_rag
from ai.rag.retriever import Retriever
from ai.agent.agent import Agent

router = APIRouter(route_class=DishkaRoute)

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(
    req: ChatRequest,
    agent: FromDishka[Agent]
):
    return {"response": await agent.chat(req.message)}

@router.post("/sync")
async def sync_endpoint(
    retriever: FromDishka[Retriever],
):
    await sync_notion_to_rag(retriever)
    return {"status": "ok"}