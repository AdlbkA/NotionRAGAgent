from dishka import Provider, Scope, provide, AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider
from ai.notion.client import NotionClient
from ai.rag.retriever import Retriever
from ai.rag.indexer import Indexer
from ai.agent.agent import Agent
from config.settings import Settings

class AppProvider(Provider):
    scope = Scope.APP

    @provide
    def settings(self) -> Settings:
        return Settings()
    
    @provide
    def notion_client(self) -> NotionClient:
        return NotionClient()

    @provide
    def retriever(self) -> Retriever:
        return Retriever()

    @provide
    def indexer(self, retriever: Retriever) -> Indexer:
        return Indexer(retriever)

    @provide
    def agent(self, retriever: Retriever, notion: NotionClient) -> Agent:
        return Agent(retriever, notion)
    
def setup_providers() -> list[Provider]:
    return [
        AppProvider()
    ]

def setup_di() -> AsyncContainer:
    container = make_async_container(
        *setup_providers()
    )

    return container

def setup_http_di() -> AsyncContainer:
    container = make_async_container(
        *setup_providers(),
        FastapiProvider()
    )
    
    return container