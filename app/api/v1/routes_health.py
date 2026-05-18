from fastapi import APIRouter

router = APIRouter(tags=["Состояние сервиса"])


@router.get("/health")
async def health_check() -> dict:
    return {
        "status": "ok",
        "service": "Sudoku API",
    }
