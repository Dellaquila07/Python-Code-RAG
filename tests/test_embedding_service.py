import types
import unittest

from types import SimpleNamespace
from unittest.mock import Mock

from tests.module_loader import import_fresh, patched_module


class TestEmbeddingService(unittest.TestCase):

    def test_generate_embeddings_stores_vectors_in_collection(self):
        fake_embeddings_api = Mock()
        fake_embeddings_api.create.return_value = SimpleNamespace(
            data=[
                SimpleNamespace(embedding=[0.1, 0.2]),
                SimpleNamespace(embedding=[0.3, 0.4]),
            ]
        )
        fake_openai_client = SimpleNamespace(embeddings=fake_embeddings_api)
        fake_collection = Mock()

        fake_dependencies_module = types.ModuleType("app.core.dependencies")
        fake_dependencies_module.dependencies = SimpleNamespace(
            openai_client=fake_openai_client,
            collection=fake_collection,
        )

        with patched_module("app.core.dependencies", fake_dependencies_module):
            module = import_fresh("app.embeddings.embedding_service")
            service = module.EmbeddingService()

            documents = [
                {"content": "def a(): pass", "metadata": {"name": "a"}},
                {"content": "def b(): pass", "metadata": {"name": "b"}},
            ]

            service.generate_embeddings(documents)

        fake_embeddings_api.create.assert_called_once_with(
            model="text-embedding-3-small",
            input=["def a(): pass", "def b(): pass"],
        )

        self.assertEqual(fake_collection.add.call_count, 1)
        call_kwargs = fake_collection.add.call_args.kwargs
        self.assertEqual(len(call_kwargs["ids"]), 2)
        self.assertEqual(call_kwargs["documents"], ["def a(): pass", "def b(): pass"])
        self.assertEqual(call_kwargs["metadatas"], [{"name": "a"}, {"name": "b"}])
        self.assertEqual(call_kwargs["embeddings"], [[0.1, 0.2], [0.3, 0.4]])


if __name__ == "__main__":
    unittest.main()
