import os
import json
import logging
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from config.settings import settings

log = logging.getLogger(name=__name__)

class NotionMCPClient:
    
    async def _call(self, tool: str, args: dict):
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@notionhq/notion-mcp-server"],
            env={
                **os.environ,
                "OPENAPI_MCP_HEADERS": json.dumps({
                    "Authorization": f"Bearer {settings.notion_token}",
                    "Notion-Version": "2025-09-03"
                })
            }
        )

        async with stdio_client(server_params) as (r, w):
            async with ClientSession(r, w) as session:
                await session.initialize()
                result = await session.call_tool(tool, args)
                return result.content[0].text
            
    async def search(self, query: str) -> str:
        return await self._call('API-post-search', {'query': query})
    
    async def fetch_page(self, page_id: str) -> str:
        return await self._call('API-retrieve-a-page', {'page_id': page_id})
    
    async def get_page_content(self, block_id: str) -> str:
        return await self._call("API-get-block-children", {
            "block_id": block_id
        })
    
    async def create_page(self, title: str, content: str, parent_id: str) -> str:
        return await self._call("API-post-page", {
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
        return await self._call("API-patch-page", {
            'page_id': page_id,
            'properties': {
                'title': {
                    'title': [{'text': {'content': title}}]
                }
            }
        })

    async def append_content(self, content: str, page_id: str) -> str:
        return await self._call("API-patch-block-children", {
            'block_id': page_id,
            'children': [
                {
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'rich_text': [
                            {
                                'type': 'text',
                                'text': {'content': content}
                            }
                        ]
                    }
                }
            ]
        })

    async def delete_block(self, block_id: str) -> str:
        return await self._call("API-delete-a-block", {
            'block_id': block_id
        })

    async def clear_page_content(self, page_id: str) -> None:
        raw = await self.get_page_content(block_id=page_id)
        children = json.loads(raw).get('results', [])
        for block in children:
            await self.delete_block(block_id=block['id'])

notion = NotionMCPClient()