from app.core.dependencies import dependencies
from typing import Dict, List


DEFAULT_CONTEXT = """
File: {0}
Type: {1}
Name: {2}
Lines: {3} - {4}

Code:
{5}
"""

DEFAULT_PROMPT = """
You are a senior software engineer helping explain a codebase.

Answer the user's question using ONLY the provided code context.

User Question:
{0}

Code Context:
{1}

Provide a clear explanation of how the code works.
"""


class CodeExplainer:

    def __init__(self):
        """ Initialize the OpenAI client """
        self.client = dependencies.openai_client

    def explain(self, question: str, chunks: List[Dict]) -> str:
        """ Generate an explanation for a codebase question """
        context = self._build_context(chunks)

        prompt = DEFAULT_PROMPT.format(question, context)

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You explain software architecture and code."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    def _build_context(self, chunks: List[Dict]) -> str:
        """ Build the textual context from retrieved chunks """
        context_parts = []

        for chunk in chunks:
            meta = chunk["metadata"]

            context_parts.append(
                DEFAULT_CONTEXT.format(
                    meta['file_path'],
                    meta['type'],
                    meta['name'],
                    meta['start_line'],
                    meta['end_line'],
                    chunk['content']
                )
            )

        return "\n\n".join(context_parts)
