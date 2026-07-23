import os
import requests

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")


class APIClient:

    # ---------------------------
    # Authentication
    # ---------------------------

    @staticmethod
    def register(username, email, password):

        payload = {
            "username": username,
            "email": email,
            "password": password
        }

        return requests.post(
            f"{BASE_URL}/auth/register",
            json=payload
        )

    @staticmethod
    def login(email, password):

        payload = {
            "email": email,
            "password": password
        }

        return requests.post(
            f"{BASE_URL}/auth/login",
            json=payload
        )

    # ---------------------------
    # Repository
    # ---------------------------

    @staticmethod
    def fetch_repository(owner, repo, token):

        headers = {
            "Authorization": f"Bearer {token}"
        }

        return requests.post(
            f"{BASE_URL}/repository/fetch",
            params={
                "owner": owner,
                "repo": repo
            },
            headers=headers
        )

    # ---------------------------
    # Analytics
    # ---------------------------

    @staticmethod
    def get_analytics(repository_id, token):

        headers = {
            "Authorization": f"Bearer {token}"
        }

        return requests.get(
            f"{BASE_URL}/analytics/{repository_id}",
            headers=headers
        )

    # ---------------------------
    # Contributors
    # ---------------------------

    @staticmethod
    def get_contributors(repository_id, token):

        headers = {
            "Authorization": f"Bearer {token}"
        }

        return requests.get(
            f"{BASE_URL}/contributors/{repository_id}",
            headers=headers
        )

    # ---------------------------
    # Commits
    # ---------------------------

    @staticmethod
    def get_commits(repository_id, token):

        headers = {
            "Authorization": f"Bearer {token}"
        }

        return requests.get(
            f"{BASE_URL}/commits/{repository_id}",
            headers=headers
        )

    # ---------------------------
    # Issues
    # ---------------------------

    @staticmethod
    def get_issues(repository_id, token):

        headers = {
            "Authorization": f"Bearer {token}"
        }

        return requests.get(
            f"{BASE_URL}/issues/{repository_id}",
            headers=headers
        )

    # ---------------------------
    # Pull Requests
    # ---------------------------

    @staticmethod
    def get_pull_requests(repository_id, token):

        headers = {
            "Authorization": f"Bearer {token}"
        }

        return requests.get(
            f"{BASE_URL}/pull-requests/{repository_id}",
            headers=headers
        )