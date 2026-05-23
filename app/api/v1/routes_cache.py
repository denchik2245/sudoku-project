from fastapi import APIRouter

from app.services.cache_service import CacheService

router = APIRouter(prefix="/cache", tags=["Cache"])


@router.get("/ping")
async def cache_ping() -> dict:
    cache = CacheService()
    await cache.set("cache:test", {"status": "ok"}, expire=60)
    value = await cache.get("cache:test")
    await cache.close()

    return {
        "redis": "connected",
        "value": value,
    }