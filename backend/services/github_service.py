import httpx
import base64
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class GitHubService:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"

    async def get_user_repos(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/user/repos?sort=updated&per_page=100", headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def get_repo_readme(self, owner: str, repo: str) -> Optional[str]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/repos/{owner}/{repo}/readme", headers=self.headers)
                if response.status_code == 200:
                    content_b64 = response.json().get("content", "")
                    return base64.b64decode(content_b64).decode("utf-8")
            except Exception:
                return None
            return None

    async def get_repo_tree(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                # Get the default branch first
                repo_info = await client.get(f"{self.base_url}/repos/{owner}/{repo}", headers=self.headers)
                default_branch = repo_info.json().get("default_branch", "main")
                
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1", 
                    headers=self.headers
                )
                if response.status_code == 200:
                    tree = response.json().get("tree", [])
                    # Filter and limit tree size for LLM analysis
                    return tree[:100]  # Just top 100 files/folders for now
            except Exception:
                return []
            return []

    async def get_repo_commits(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/commits?per_page=20", 
                    headers=self.headers
                )
                if response.status_code == 200:
                    return response.json()
            except Exception:
                return []
            return []
