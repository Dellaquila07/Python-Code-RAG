import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """ Application configuration settings """

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    CHROMA_COLLECTION: str = "codebase"
    CHROMA_PATH: str = "./data/chroma"


settings = Settings()
