import uuid

from app.core.dependencies import dependencies
from typing import Dict, List


class EmbeddingService:

    def __init__(self):
        """ Initialize the embedding service """
        self.client = dependencies.openai_client
        self.collection = dependencies.collection

    def generate_embeddings(self, documents: List[Dict]) -> None:
        """
        Generate embeddings for a list of documents
        and store them in ChromaDB
        """
        ids = []
        contents = []
        metadatas = []

        for doc in documents:
            ids.append(str(uuid.uuid4()))
            contents.append(doc["content"])
            metadatas.append(doc["metadata"])

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=contents
        )

        embeddings = [item.embedding for item in response.data]

        self.add_documents(
            ids=ids,
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas
        )
