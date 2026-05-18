from fastapi import APIRouter

from app.api.v1.routes_cache import router as cache_router
from app.api.v1.routes_debug import router as debug_router
from app.api.v1.routes_games import router as games_router
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_sudoku import router as sudoku_router
from app.api.v1.routes_tasks import router as tasks_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(debug_router)
api_router.include_router(cache_router)
api_router.include_router(games_router)
api_router.include_router(sudoku_router)
api_router.include_router(tasks_router)
