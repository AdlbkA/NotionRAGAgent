# NotionRAGAgent

RAG (Retrieval Augmented Generation) system for interacting with Notion via the Notion REST API and Claude AI.

## Overview

NotionRAGAgent is an integration of Notion with LLM that enables:
- Synchronize documents from Notion to a vector database
- Perform semantic search on indexed content
- Answer questions using context from Notion (RAG)
- Create pages based on user requirements
- Interact via REST API

The system talks directly to the Notion REST API for reading and writing pages and uses ChromaDB for storing vector embeddings.

## Tech Stack

- **Python 3.13+** — primary language
- **FastAPI** — REST API server
- **Anthropic Claude** — LLM for answer generation
- **LlamaIndex** — indexing and search framework
- **ChromaDB** — vector database
- **Sentence Transformers** — embeddings generation
- **Notion REST API** — Notion integration (via `httpx`)

## Project Structure

```
.
├── ai/                     # AI core modules
│   ├── agent/             # AI agent implementation
│   │   ├── agent.py       # Main agent logic with Claude
│   │   ├── prompts.py     # System prompts
│   │   └── tools.py       # Agent tools and utilities
│   ├── notion/            # Notion REST API integration
│   │   ├── client.py      # Client for the Notion REST API
│   │   └── sync.py        # Notion → RAG synchronization
│   └── rag/               # RAG (Retrieval Augmented Generation)
│       ├── embeddings.py  # Embeddings generation model
│       ├── indexer.py     # Document indexing to ChromaDB
│       └── retriever.py   # Semantic search functionality
├── src/                   # Main application source code
│   ├── main.py            # Application entry point
│   ├── di.py              # Dependency injection setup
│   └── api/               # REST API layer
│       └── read.py        # Read API endpoints
├── config/                # Configuration management
│   └── settings.py        # Application settings from environment variables
├── storage/               # Data storage
│   └── chroma/           # ChromaDB vector database
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker Compose orchestration
├── pyproject.toml         # Project dependencies and metadata
```

## Installation

### Prerequisites
- Python 3.13+
- Notion workspace with API token
- Anthropic API key

### Installation Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd NotionRAGAgent
```

2. **Install dependencies:**
```bash
uv sync
```

Or alternatively with pip:
```bash
pip install -e .
```

3. **Create `.env` file:**
```bash
NOTION_TOKEN=your_notion_api_token
ANTHROPIC_API_KEY=your_anthropic_api_key
CHROMA_PATH=./storage/chroma
```

How to get tokens:
- **Notion Token**: https://www.notion.so/my-integrations
- **Anthropic API Key**: https://console.anthropic.com/

## Usage

### Starting the Server

```bash
uvicorn src.main:app --reload
```

The server will be available at `http://localhost:8000`

### API Endpoints

#### 1. Document Synchronization from Notion
```bash
POST /sync
```

Loads all documents from Notion into the vector database for indexing.

**Example:**
```bash
curl -X POST http://localhost:8000/sync
```

**Response:**
```json
{"status": "ok"}
```

#### 2. Chat with RAG Context
```bash
POST /chat
```

Sends a question and receives an answer based on context from Notion.

**Example:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is MCP?"}'
```

**Response:**
```json
{"response": "MCP (Model Context Protocol) is a protocol..."}
```

## Architecture

### Data Flow

1. **Synchronization (Sync)**
   ```
   Notion REST API → NotionClient
   → Documents [id, title, content]
   → LlamaIndex: Document objects
   → Embeddings (Sentence Transformers)
   → ChromaDB (Persistent storage)
   ```

2. **Search and Answer (RAG)**
   ```
   User Query
   → Embedding
   → Semantic Search in ChromaDB (top_k=5)
   → Context chunks
   → Claude LLM with System Prompt
   → Answer
   ```

## Configuration

All parameters are read from the `.env` file:

```env
# Notion API token (get from https://www.notion.so/my-integrations)
NOTION_TOKEN=ntp_xxx...

# Anthropic API key (get from https://console.anthropic.com/)
ANTHROPIC_API_KEY=sk-ant-...

# Path to ChromaDB storage (optional)
CHROMA_PATH=./storage/chroma

# HuggingFace token for faster model loading (optional)
HF_TOKEN=
```

## Troubleshooting

### ChromaDB connection fails
- Ensure that the `./storage/chroma` directory exists and is writable
- Make sure `CHROMA_PATH` in `.env` points to the correct path

### Notion API errors
- Verify that `NOTION_TOKEN` is correct
- Check that the integration has access permissions in your Notion workspace (share the pages/databases with your integration)
- If needed, override the API version via `NOTION_VERSION` (defaults to `2022-06-28`)
