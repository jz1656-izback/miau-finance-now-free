"""Social module for the Miau Finance Python SDK."""

from typing import Optional

from miau import MiauClient


class SocialModule:
    """Access social, feed, and community endpoints."""

    def __init__(self, client: MiauClient):
        self._client = client

    def get_feed(self, scope: str = "global", limit: int = 20, offset: int = 0) -> list[dict]:
        return self._client.get("/api/v1/social/feed", {"scope": scope, "limit": limit, "offset": offset})

    def share_portfolio(self, portfolio_id: str, message: str = "") -> dict:
        return self._client.post("/api/v1/social/share", {"portfolio_id": portfolio_id, "message": message})

    def get_comments(self, activity_id: str) -> list[dict]:
        return self._client.get(f"/api/v1/social/comments/{activity_id}")

    def post_comment(self, activity_id: str, content: str) -> dict:
        return self._client.post(f"/api/v1/social/comments/{activity_id}", {"content": content})

    def follow(self, username: str) -> dict:
        return self._client.post("/api/v1/social/follow", {"username": username})

    def unfollow(self, username: str) -> dict:
        return self._client.post("/api/v1/social/unfollow", {"username": username})

    def get_profile(self, username: Optional[str] = None) -> dict:
        params = {}
        if username:
            params["username"] = username
        return self._client.get("/api/v1/social/profile", params)

    def get_leaderboard(self, metric: str = "total_return") -> list[dict]:
        return self._client.get("/api/v1/social/leaderboard", {"metric": metric})
