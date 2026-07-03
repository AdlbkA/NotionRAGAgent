from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    notion_token: str
    notion_version: str = '2022-06-28'
    anthropic_api_key: str
    chroma_path: str = './storage/chroma'
    hf_token: str

    class Config:
        env_file = '.env'

settings = Settings()