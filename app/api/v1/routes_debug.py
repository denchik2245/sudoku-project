from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter(tags=["Debug"])


@router.get("/debug/db")
async def debug_db(session: AsyncSession = Depends(get_db)) -> dict:
    result = await session.execute(text("SELECT 1"))
    value = result.scalar_one()

    return {
        "database": "connected",
        "result": value,
    }
