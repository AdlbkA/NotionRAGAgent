# NotionMCP

RAG (Retrieval Augmented Generation) система для взаимодействия с Notion через Model Context Protocol и Claude AI.

## Описание

NotionMCP — это интеграция Notion с LLM, которая позволяет:
- Синхронизировать документы из Notion в векторную базу данных
- Выполнять семантический поиск по индексированному контенту
- Отвечать на вопросы с использованием контекста из Notion (RAG)
- Взаимодействовать через REST API

Система использует Model Context Protocol (MCP) для безопасного подключения к Notion API и ChromaDB для хранения векторных эмбеддингов.

## Технологический стек

- **Python 3.13+** — основной язык
- **FastAPI** — REST API сервер
- **Anthropic Claude** — LLM для генерации ответов
- **LlamaIndex** — фреймворк для индексирования и поиска
- **ChromaDB** — векторная база данных
- **Sentence Transformers** — генерирование эмбеддингов
- **MCP (Model Context Protocol)** — интеграция с Notion

## Структура проекта

```
.
├── api/                    # REST API endpoints
│   └── main.py            # FastAPI приложение
├── mcp_conf/              # MCP конфигурация и интеграция
│   ├── notion_client.py   # Клиент для работы с Notion API через MCP
│   └── sync.py            # Синхронизация Notion → RAG
├── rag/                   # RAG (Retrieval Augmented Generation)
│   ├── embeddings.py      # Модель для генерирования эмбеддингов
│   ├── indexer.py         # Индексирование документов в ChromaDB
│   └── retriever.py       # Семантический поиск
├── agent/                 # AI агент
│   ├── agent.py           # Основная логика агента с Claude
│   └── prompts.py         # Системные промпты
├── config/                # Конфигурация
│   └── settings.py        # Параметры приложения из переменных окружения
├── storage/               # Локальное хранилище
│   └── chroma/           # БД ChromaDB
├── pyproject.toml         # Зависимости проекта
└── README.md             # Этот файл
```

## Установка

### Предварительные требования
- Python 3.13+
- Notion workspace с API token
- Anthropic API key

### Шаги установки

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd NotionMCP
```

2. **Установите зависимости:**
```bash
uv sync
```

Или альтернативно через pip:
```bash
pip install -e .
```

3. **Создайте файл `.env`:**
```bash
NOTION_TOKEN=your_notion_api_token
ANTHROPIC_API_KEY=your_anthropic_api_key
CHROMA_PATH=./storage/chroma
```

Как получить токены:
- **Notion Token**: https://www.notion.so/my-integrations
- **Anthropic API Key**: https://console.anthropic.com/

## Использование

### Запуск сервера

```bash
cd api
uvicorn main:app --reload
```

Сервер будет доступен на `http://localhost:8000`

### API Endpoints

#### 1. Синхронизация документов из Notion
```bash
POST /sync
```

Загружает все документы из Notion в векторную БД для индексирования.

**Пример:**
```bash
curl -X POST http://localhost:8000/sync
```

**Ответ:**
```json
{"status": "ok"}
```

#### 2. Chat с RAG контекстом
```bash
POST /chat
```

Отправляет вопрос, получает ответ на основе контекста из Notion.

**Пример:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Что такое MCP?"}'
```

**Ответ:**
```json
{"response": "MCP (Model Context Protocol) — это протокол..."}
```

## Архитектура

### Поток данных

1. **Синхронизация (Sync)**
   ```
   Notion API (MCP) → NotionMCPClient
   → Документы [id, title, content]
   → LlamaIndex: Document objects
   → Embeddings (Sentence Transformers)
   → ChromaDB (Persistent storage)
   ```

2. **Поиск и Ответ (RAG)**
   ```
   User Query
   → Embedding
   → Semantic Search in ChromaDB (top_k=5)
   → Context chunks
   → Claude LLM with System Prompt
   → Answer
   ```

## Конфигурация

Все параметры считываются из файла `.env`:

```env
# Notion API токен (получить на https://www.notion.so/my-integrations)
NOTION_TOKEN=ntp_xxx...

# Anthropic API ключ (получить на https://console.anthropic.com/)
ANTHROPIC_API_KEY=sk-ant-...

# Путь к хранилищу ChromaDB (опционально)
CHROMA_PATH=./storage/chroma
```

## Troubleshooting

### ChromaDB не подключается
- Проверьте, что директория `./storage/chroma` существует и доступна для записи
- Убедитесь, что `CHROMA_PATH` в `.env` указывает на правильный путь

### Ошибки с Notion API
- Проверьте, что `NOTION_TOKEN` корректен
- Убедитесь, что MCP сервер Notion установлен (`npm install -g @notionhq/notion-mcp-server`)
- Проверьте права доступа интеграции в Notion workspace
