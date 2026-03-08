from dotenv import load_dotenv

from app.ingestion.repo_cloner import RepoCloner
from app.ingestion.code_loader import CodeLoader
from app.ingestion.code_parser import CodeParser
from app.ingestion.code_chunker import CodeChunker

from app.embeddings.embedding_service import EmbeddingService
from app.retrieval.retriever import Retriever
from app.llm.code_explainer import CodeExplainer

load_dotenv()


def index_repository(repo_url: str):
    """ Full indexing pipeline for a GitHub repository """
    cloner = RepoCloner()
    repo_path = cloner.clone(repo_url)

    loader = CodeLoader()
    files = loader.load_files(repo_path)

    parser = CodeParser()

    blocks = []
    for file in files:
        blocks.extend(parser.parse_file(file))

    chunker = CodeChunker()
    documents = chunker.create_chunks(blocks)

    embedding_service = EmbeddingService()
    embedding_service.generate_embeddings(documents)


def ask_question(question: str):
    """ Query the indexed codebase """
    retriever = Retriever()
    explainer = CodeExplainer()

    chunks = retriever.retrieve(question)
    answer = explainer.explain(question, chunks)

    return answer


def main():
    """Run indexing and answer a user question from terminal input."""
    repo_url = input("Please provide the repository URL: ").strip()
    if not repo_url:
        raise ValueError("The repository URL cannot be empty.")

    index_repository(repo_url)

    question = input("Type your question about the code: ").strip()
    if not question:
        raise ValueError("The question cannot be empty.")

    answer = ask_question(question)
    print(answer)


if __name__ == "__main__":
    main()
