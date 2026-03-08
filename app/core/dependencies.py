import chromadb

from app.core.config import settings
from chromadb.config import Settings as ChromaSettings
from openai import OpenAI


class Dependencies:
    """ Dependency container for shared services """

    def __init__(self):
        """ Configure dependencies """
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PATH,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION
        )


dependencies = Dependencies()
