import ast

from pathlib import Path
from typing import Dict, List


class CodeParser:

    def parse_file(self, file_path: Path) -> List[Dict]:
        """ Parse a Python file and extract functions and classes """
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        blocks = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                blocks.append(
                    self._extract_block(
                        node,
                        source,
                        file_path,
                        "function"
                    )
                )
            elif isinstance(node, ast.ClassDef):
                blocks.append(
                    self._extract_block(
                        node,
                        source,
                        file_path,
                        "class"
                    )
                )

        return blocks

    def _extract_block(
        self,
        node: ast.ClassDef | ast.FunctionDef,
        source: str,
        file_path: Path,
        block_type: str
    ) -> Dict:
        """ Extract code block information from an AST node """
        lines = source.splitlines()

        start_line = node.lineno
        end_line = getattr(node, "end_lineno", node.lineno)

        code = "\n".join(lines[start_line - 1:end_line])

        return {
            "type": block_type,
            "name": node.name,
            "file_path": str(file_path),
            "start_line": start_line,
            "end_line": end_line,
            "code": code
        }
