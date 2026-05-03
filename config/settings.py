from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    notion_token: str
    anthropic_api_key: str
    chroma_path: str = './storage/chroma'

    class Config:
        env_file = '.env'

settings = Settings()