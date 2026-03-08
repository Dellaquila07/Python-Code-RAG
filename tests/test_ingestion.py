import ast
import types
import unittest

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from tests.module_loader import import_fresh, patched_module


class TestIngestion(unittest.TestCase):

    def test_repo_cloner_uses_existing_path_without_clone(self):
        fake_repo_class = types.SimpleNamespace(clone_from=Mock())
        fake_git_module = types.ModuleType("git")
        fake_git_module.Repo = fake_repo_class

        with TemporaryDirectory() as tmp_dir:
            with patched_module("git", fake_git_module):
                module = import_fresh("app.ingestion.repo_cloner")
                cloner = module.RepoCloner(base_path=tmp_dir)

                existing = Path(tmp_dir) / "my-repo"
                existing.mkdir()

                result = cloner.clone("https://github.com/org/my-repo.git")

            self.assertEqual(result, existing)
            fake_repo_class.clone_from.assert_not_called()

    def test_repo_cloner_clones_when_path_does_not_exist(self):
        fake_repo_class = types.SimpleNamespace(clone_from=Mock())
        fake_git_module = types.ModuleType("git")
        fake_git_module.Repo = fake_repo_class

        with TemporaryDirectory() as tmp_dir:
            with patched_module("git", fake_git_module):
                module = import_fresh("app.ingestion.repo_cloner")
                cloner = module.RepoCloner(base_path=tmp_dir)
                result = cloner.clone("https://github.com/org/new-repo")

            expected = Path(tmp_dir) / "new-repo"
            self.assertEqual(result, expected)
            fake_repo_class.clone_from.assert_called_once_with(
                "https://github.com/org/new-repo",
                expected,
            )

    def test_code_loader_filters_supported_extensions(self):
        module = import_fresh("app.ingestion.code_loader")
        loader = module.CodeLoader()

        with TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "a.py").write_text("print('x')", encoding="utf-8")
            (root / "b.ts").write_text("export const x = 1", encoding="utf-8")
            (root / "c.md").write_text("# docs", encoding="utf-8")

            files = loader.load_files(root)

        names = sorted(path.name for path in files)
        self.assertEqual(names, ["a.py", "b.ts"])

    def test_code_parser_extracts_function_and_class_blocks(self):
        module = import_fresh("app.ingestion.code_parser")
        parser = module.CodeParser()

        with TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "sample.py"
            file_path.write_text(
                "def greet():\n"
                "    return 'hello'\n\n"
                "class User:\n"
                "    pass\n",
                encoding="utf-8",
            )

            blocks = parser.parse_file(file_path)

        block_names = sorted((block["type"], block["name"]) for block in blocks)
        self.assertIn(("function", "greet"), block_names)
        self.assertIn(("class", "User"), block_names)

    def test_code_chunker_builds_content_with_metadata(self):
        module = import_fresh("app.ingestion.code_chunker")
        chunker = module.CodeChunker()

        docs = chunker.create_chunks(
            [
                {
                    "type": "function",
                    "name": "greet",
                    "file_path": "src/sample.py",
                    "start_line": 1,
                    "end_line": 2,
                    "code": "def greet():\n    return 'hello'",
                }
            ]
        )

        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]["metadata"]["name"], "greet")
        self.assertIn("Function greet defined in file src/sample.py", docs[0]["content"])


if __name__ == "__main__":
    unittest.main()
