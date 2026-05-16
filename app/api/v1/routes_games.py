from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.game import (
    CellCheckResponse,
    GameCheckResponse,
    GameCreateRequest,
    GameMoveRequest,
    GameMoveResponse,
    GamePublicDetailResponse,
)
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["Игры"])


@router.post("", response_model=GamePublicDetailResponse)
async def create_game(
    payload: GameCreateRequest,
    session: AsyncSession = Depends(get_db),
) -> GamePublicDetailResponse:
    service = GameService(session)
    game = await service.create_game(payload.difficulty)
    return service.build_game_public_response(game)


@router.get("/{game_id}", response_model=GamePublicDetailResponse)
async def get_game(
    game_id: int,
    session: AsyncSession = Depends(get_db),
) -> GamePublicDetailResponse:
    service = GameService(session)
    game = await service.get_game(game_id)
    return service.build_game_public_response(game)


@router.post("/{game_id}/move", response_model=GameMoveResponse)
async def make_move(
    game_id: int,
    payload: GameMoveRequest,
    session: AsyncSession = Depends(get_db),
) -> GameMoveResponse:
    service = GameService(session)
    return await service.make_move(
        game_id=game_id,
        row=payload.row,
        col=payload.col,
        value=payload.value,
    )


@router.get("/{game_id}/check", response_model=GameCheckResponse)
async def check_game(
    game_id: int,
    session: AsyncSession = Depends(get_db),
) -> GameCheckResponse:
    service = GameService(session)
    return await service.check_game(game_id)


@router.get("/{game_id}/check-cell", response_model=CellCheckResponse)
async def check_cell(
    game_id: int,
    row: int,
    col: int,
    session: AsyncSession = Depends(get_db),
) -> CellCheckResponse:
    service = GameService(session)
    return await service.check_cell(game_id, row, col)


@router.post("/{game_id}/solve", response_model=GamePublicDetailResponse)
async def solve_game(
    game_id: int,
    session: AsyncSession = Depends(get_db),
) -> GamePublicDetailResponse:
    service = GameService(session)
    return await service.solve_game(game_id)