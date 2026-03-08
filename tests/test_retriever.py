import types
import unittest

from types import SimpleNamespace
from unittest.mock import Mock

from tests.module_loader import import_fresh, patched_module


class TestRetriever(unittest.TestCase):

    def test_retrieve_returns_content_and_metadata_pairs(self):
        fake_embeddings_api = Mock()
        fake_embeddings_api.create.return_value = SimpleNamespace(
            data=[SimpleNamespace(embedding=[0.9, 0.8])]
        )
        fake_openai_client = SimpleNamespace(embeddings=fake_embeddings_api)

        fake_collection = Mock()
        fake_collection.query.return_value = {
            "documents": [["code chunk 1", "code chunk 2"]],
            "metadatas": [[{"file_path": "a.py"}, {"file_path": "b.py"}]],
        }

        fake_dependencies_module = types.ModuleType("app.core.dependencies")
        fake_dependencies_module.dependencies = SimpleNamespace(
            openai_client=fake_openai_client,
            collection=fake_collection,
        )

        with patched_module("app.core.dependencies", fake_dependencies_module):
            module = import_fresh("app.retrieval.retriever")
            retriever = module.Retriever()
            result = retriever.retrieve("How does auth work?", k=2)

        fake_embeddings_api.create.assert_called_once_with(
            model="text-embedding-3-small",
            input="How does auth work?",
        )
        fake_collection.query.assert_called_once_with(
            query_embeddings=[[0.9, 0.8]],
            n_results=2,
        )

        self.assertEqual(
            result,
            [
                {"content": "code chunk 1", "metadata": {"file_path": "a.py"}},
                {"content": "code chunk 2", "metadata": {"file_path": "b.py"}},
            ],
        )


if __name__ == "__main__":
    unittest.main()
