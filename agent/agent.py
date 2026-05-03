import anthropic
import os
import json
from config.settings import settings
from rag.retriever import retrieve
from agent.prompts import SYSTEM_PROMPT

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

async def chat(user_message: str) -> str:
    chunks = retrieve(user_message, top_k=50)
    rag_context = '\n\n'.join(
        f"[{c['title']}]\n{c['text']}" for c in chunks
    )

    augmented_message = f"""Контекст из Notion (RAG):
---
{rag_context}
---

Вопрос пользователя: {user_message}
"""
    response = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=5000,
        system=SYSTEM_PROMPT,
        messages=[{'role': 'user', 'content': augmented_message}]
    )

    return response.content[0].text


