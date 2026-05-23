import hashlib
import json

import redis.asyncio as redis

from app.core.config import settings


class CacheService:
    def __init__(self):
        self.redis = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: dict, expire: int = 300) -> None:
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def close(self) -> None:
        await self.redis.close()

    @staticmethod
    def make_solve_key(board: list[list[int]]) -> str:
        board_string = json.dumps(board, sort_keys=True)
        board_hash = hashlib.md5(board_string.encode()).hexdigest()
        return f"sudoku:solve:{board_hash}"

    @staticmethod
    def make_generate_key(difficulty: str) -> str:
        return f"sudoku:generate:{difficulty}"