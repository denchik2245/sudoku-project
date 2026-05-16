from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.game import SudokuGame
from app.db.models.move import SudokuMove


class GameRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_game(
        self,
        initial_board: str,
        current_board: str,
        solution: str,
        difficulty: str,
        status: str = "new",
    ) -> SudokuGame:
        game = SudokuGame(
            initial_board=initial_board,
            current_board=current_board,
            solution=solution,
            difficulty=difficulty,
            status=status,
        )
        self.session.add(game)
        await self.session.commit()
        await self.session.refresh(game)
        return game

    async def get_game_by_id(self, game_id: int) -> SudokuGame | None:
        result = await self.session.execute(
            select(SudokuGame)
            .options(selectinload(SudokuGame.moves))
            .where(SudokuGame.id == game_id)
        )
        return result.scalar_one_or_none()

    async def update_current_board(
        self,
        game: SudokuGame,
        current_board: str,
        status: str | None = None,
    ) -> SudokuGame:
        game.current_board = current_board
        if status is not None:
            game.status = status

        await self.session.commit()
        await self.session.refresh(game)
        return game

    async def create_move(
        self,
        game_id: int,
        row: int,
        col: int,
        value: int,
        is_valid: bool,
    ) -> SudokuMove:
        move = SudokuMove(
            game_id=game_id,
            row=row,
            col=col,
            value=value,
            is_valid=is_valid,
        )
        self.session.add(move)
        await self.session.commit()
        await self.session.refresh(move)
        return move