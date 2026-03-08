from pathlib import Path
from typing import List


class CodeLoader:

    SUPPORTED_EXTENSIONS = [
        ".py",
        ".ts",
        ".js",
        ".java",
        ".go",
        ".rs"
    ]

    def load_files(self, repo_path: Path) -> List[Path]:
        """ Load project files """
        files = []

        for path in repo_path.rglob("*"):
            if path.suffix in self.SUPPORTED_EXTENSIONS:
                files.append(path)

        return files
