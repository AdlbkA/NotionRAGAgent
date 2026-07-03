import json
import logging

import httpx

from config.settings import settings

log = logging.getLogger(name=__name__)

NOTION_API_URL = "https://api.notion.com/v1"


class NotionClient:

    def __init__(self, token: str | None = None, version: str | None = None):
        self._token = token or settings.notion_token
        self._version = version or settings.notion_version

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._token}",
            "Notion-Version": self._version,
            "Content-Type": "application/json",
        }

    async def _request(self, method: str, path: str, json_body: dict | None = None) -> str:
        url = f"{NOTION_API_URL}{path}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method,
                url,
                headers=self._headers,
                json=json_body,
            )
        if response.status_code >= 400:
            log.warning("Notion API %s %s -> %s: %s", method, path, response.status_code, response.text)
        return response.text

    async def search(self, query: str) -> str:
        return await self._request("POST", "/search", {"query": query})

    async def fetch_page(self, page_id: str) -> str:
        return await self._request("GET", f"/pages/{page_id}")

    async def get_page_content(self, block_id: str) -> str:
        return await self._request("GET", f"/blocks/{block_id}/children?page_size=100")

    async def create_page(self, title: str, content: str, parent_id: str) -> str:
        return await self._request("POST", "/pages", {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content}
                            }
                        ]
                    }
                }
            ]
        })

    async def rename_page(self, title: str, page_id: str) -> str:
        return await self._request("PATCH", f"/pages/{page_id}", {
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            }
        })

    async def append_content(self, content: str, page_id: str) -> str:
        return await self._request("PATCH", f"/blocks/{page_id}/children", {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content}
                            }
                        ]
                    }
                }
            ]
        })

    async def delete_block(self, block_id: str) -> str:
        return await self._request("DELETE", f"/blocks/{block_id}")

    async def clear_page_content(self, page_id: str) -> None:
        raw = await self.get_page_content(block_id=page_id)
        children = json.loads(raw).get("results", [])
        for block in children:
            await self.delete_block(block_id=block["id"])


notion = NotionClient()
