import chromadb
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from config.settings import settings
from rag.embeddings import get_embed_model

def get_vector_store():
    client = chromadb.PersistentClient(path=settings.chroma_path)
    collection = client.get_or_create_collection('notion_docs')
    return ChromaVectorStore(chroma_collection=collection)

def index_documents(pages: list[dict]) -> VectorStoreIndex:
    """
    pages - список словарей:
    [{'id': 'abc', 'title': 'Title', 'content': 'Text'}]
    """

    documents = [
        Document(
            text=p['content'],
            metadata={'notion_id': p['id'], 'title': p['title']}
        )
        for p in pages
    ]

    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=get_embed_model()
    )

    return index
