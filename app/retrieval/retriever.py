from app.core.dependencies import dependencies
from typing import Dict, List


class Retriever:

    def __init__(self):
        """ Initialize retriever with OpenAI and ChromaDB clients """
        self.client = dependencies.openai_client
        self.collection = dependencies.collection

    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """ Retrieve the most relevant code chunks for a given query """
        embedding_response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )

        query_embedding = embedding_response.data[0].embedding

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        retrieved_chunks = []

        for doc, meta in zip(documents, metadatas):
            retrieved_chunks.append(
                {
                    "content": doc,
                    "metadata": meta
                }
            )

        return retrieved_chunks
