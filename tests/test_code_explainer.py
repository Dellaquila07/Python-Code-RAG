import types
import unittest

from types import SimpleNamespace
from unittest.mock import Mock

from tests.module_loader import import_fresh, patched_module


class TestCodeExplainer(unittest.TestCase):

    def test_explain_builds_prompt_from_multiple_chunks(self):
        fake_chat_api = Mock()
        fake_chat_api.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="Mocked answer"))]
        )
        fake_openai_client = SimpleNamespace(chat=fake_chat_api)

        fake_dependencies_module = types.ModuleType("app.core.dependencies")
        fake_dependencies_module.dependencies = SimpleNamespace(
            openai_client=fake_openai_client,
        )

        chunks = [
            {
                "content": "def first(): pass",
                "metadata": {
                    "file_path": "src/first.py",
                    "type": "function",
                    "name": "first",
                    "start_line": 1,
                    "end_line": 1,
                },
            },
            {
                "content": "def second(): pass",
                "metadata": {
                    "file_path": "src/second.py",
                    "type": "function",
                    "name": "second",
                    "start_line": 5,
                    "end_line": 5,
                },
            },
        ]

        with patched_module("app.core.dependencies", fake_dependencies_module):
            module = import_fresh("app.llm.code_explainer")
            explainer = module.CodeExplainer()
            answer = explainer.explain("What do these functions do?", chunks)

        self.assertEqual(answer, "Mocked answer")
        self.assertEqual(fake_chat_api.completions.create.call_count, 1)

        prompt = fake_chat_api.completions.create.call_args.kwargs["messages"][1]["content"]
        self.assertIn("src/first.py", prompt)
        self.assertIn("src/second.py", prompt)
        self.assertIn("What do these functions do?", prompt)


if __name__ == "__main__":
    unittest.main()
