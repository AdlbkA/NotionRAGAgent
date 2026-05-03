import json
import asyncio
import chromadb
from config.settings import settings as cfg
from mcp_conf.notion_client import notion
from rag.indexer import index_documents

async def sync_notion_to_rag(query: str = ""):
    client = chromadb.PersistentClient(path=cfg.chroma_path)
    client.delete_collection("notion_docs")
    print("Chroma очищена")
    
    print("Fetching pages from Notion...")
    raw = await notion.search(query)

    try:
        data = json.loads(raw)
        results = data.get('results', [])
    except Exception:
        print('Ошибка парсинга Notion:', raw)
        return
    
    pages = []
    for item in results:
        obj_type = item.get("object", "")
        page_id = item.get("id", "")
        title = extract_title(item)


        if obj_type == "data_source":
            print(f"  ⏭ Пропускаем БД: {title}")
            continue

        try:
            blocks_raw = await notion.get_page_content(page_id)
            blocks_data = json.loads(blocks_raw)
            block_results = blocks_data.get("results", [])

            if block_results:
                content = extract_text_from_blocks(block_results)
            else:
                content = extract_content_from_properties(item)
        except Exception as e:
            content = extract_content_from_properties(item)

        if not content.strip():
            print(f"  ⏭ Нет контента: {title} ({page_id})")
            continue

        pages.append({"id": page_id, "title": title, "content": content})
        print(f"  ✓ {title}")

    print(f"Indexing {len(pages)} pages...")
    index_documents(pages)
    print("Sync complete.")

def extract_text_from_blocks(blocks: list) -> str:
    texts = []
    for block in blocks:
        block_type = block.get("type", "")
        block_data = block.get(block_type, {})
        rich_text = block_data.get("rich_text", [])
        for rt in rich_text:
            texts.append(rt.get("plain_text", ""))
    return "\n".join(texts)

def extract_title(item: dict) -> str:
    obj_type = item.get("object", "")

    if obj_type == "data_source":
        title_arr = item.get("title", [])
        if title_arr:
            return title_arr[0].get("plain_text", "Без названия")
        return "Без названия"

    for key, val in item.get("properties", {}).items():
        if val.get("id") == "title" and val.get("type") == "title":
            arr = val.get("title", [])
            if arr:
                text = arr[0].get("plain_text", "").strip()
                if text:
                    return text

    return "Без названия"

def extract_content_from_properties(item: dict) -> str:
    parts = []
    for key, val in item.get("properties", {}).items():
        prop_type = val.get("type", "")
        if prop_type in ("title", "rich_text"):
            arr = val.get(prop_type, [])
            text = " ".join(t.get("plain_text", "") for t in arr).strip()
            if text:
                parts.append(f"{key}: {text}")
        elif prop_type == "select":
            sel = val.get("select")
            if sel:
                parts.append(f"{key}: {sel.get('name', '')}")
        elif prop_type == "multi_select":
            vals = [s.get("name", "") for s in val.get("multi_select", [])]
            if vals:
                parts.append(f"{key}: {', '.join(vals)}")
        elif prop_type == "date":
            date = val.get("date")
            if date:
                parts.append(f"{key}: {date.get('start', '')}")
    return "\n".join(parts)


if __name__ == "__main__":
    asyncio.run(sync_notion_to_rag())