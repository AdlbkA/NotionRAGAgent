NOTION_TOOLS = [
    {
        "name": "create_notion_page",
        "description": "Создать новую страницу в Notion. Используй когда пользователь просит создать заметку, страницу или запись.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Заголовок страницы"
                },
                "content": {
                    "type": "string",
                    "description": "Содержимое страницы"
                },
                "parent_id": {
                    "type": "string",
                    "description": "ID родительской страницы в Notion"
                }
            },
            "required": ["title", "content", "parent_id"]
        }
    },
    {
        "name": "search_notion",
        "description": "Поиск по Notion если RAG-контекст недостаточен или нужна актуальная информация.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Поисковый запрос"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "rename_notion_page",
        "description": "Обновление контента страницы.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Заголовок страницы"
                },
                "page_id": {
                    "type": "string",
                    "description": "ID страницы в Notion"
                }
            },
            "required": ["title", "page_id"]
        }
    },
    {
        "name": "delete_notion_page",
        "description": "Удаление страницы Notion.",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {
                    "type": "string",
                    "description": "ID страницы в Notion"
                }
            },
            "required": ["page_id"]
        }
    },
    {
        "name": "append_notion_content",
        "description": "Запись информации в пустую страницу Notion.",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Содержимое странцы"
                },
                "page_id": {
                    "type": "string",
                    "description": "ID страницы в Notion"
                }
            },
            "required": ["content", "page_id"]
        }
    },
{
        "name": "edit_notion_content",
        "description": "Редактирование содержимого страницы Notion.",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Содержимое странцы"
                },
                "page_id": {
                    "type": "string",
                    "description": "ID блока в Notion"
                }
            },
            "required": ["content", "page_id"]
        }
    },
]
