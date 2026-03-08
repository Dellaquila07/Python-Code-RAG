from git import Repo
from pathlib import Path


class RepoCloner:

    def __init__(self, base_path: str = "data/repos"):
        """ Initialize the repository cloner """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def clone(self, repo_url: str) -> Path:
        """ Clone GitHub repository """
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = self.base_path / repo_name

        if repo_path.exists():
            return repo_path

        Repo.clone_from(repo_url, repo_path)

        return repo_path
