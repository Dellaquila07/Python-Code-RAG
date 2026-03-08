from typing import Dict, List


class CodeChunker:

    def create_chunks(self, code_blocks: List[Dict]) -> List[Dict]:
        """ Convert parsed code blocks into embedding-read chunks """
        documents = []

        for block in code_blocks:
            content = self._build_content(block)

            documents.append(
                {
                    "content": content,
                    "metadata": {
                        "type": block["type"],
                        "name": block["name"],
                        "file_path": block["file_path"],
                        "start_line": block["start_line"],
                        "end_line": block["end_line"]
                    }
                }
            )

        return documents

    def _build_content(self, block: Dict) -> str:
        """ Build the textual representation used for embeddings """
        header = (
            f"{block['type'].capitalize()} {block['name']} "
            f"defined in file {block['file_path']} "
            f"from line {block['start_line']} to {block['end_line']}."
        )

        return f"{header}\n\nCode:\n{block['code']}"
