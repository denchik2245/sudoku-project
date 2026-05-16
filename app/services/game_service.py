from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.game_repository import GameRepository
from app.schemas.game import (
    GameCheckResponse,
    GameMoveResponse,
    GamePublicDetailResponse,
    CellCheckResponse,
)
from app.services.sudoku_service import SudokuService
from app.utils.helpers import deserialize_board, serialize_board


class GameService:
    def __init__(self, session: AsyncSession):
        self.repository = GameRepository(session)

    async def create_game(self, difficulty: str):
        sudoku_data = await SudokuService.generate_board(difficulty)
        return await self.repository.create_game(
            initial_board=serialize_board(sudoku_data["puzzle"]),
            current_board=serialize_board(sudoku_data["puzzle"]),
            solution=serialize_board(sudoku_data["solution"]),
            difficulty=sudoku_data["difficulty"],
        )

    async def get_game(self, game_id: int):
        game = await self.repository.get_game_by_id(game_id)
        if game is None:
            raise HTTPException(status_code=404, detail="Игра не найдена")
        return game

    async def update_game_board(
        self,
        game_id: int,
        current_board: list[list[int]],
        status: str | None = None,
    ):
        game = await self.get_game(game_id)
        return await self.repository.update_current_board(
            game=game,
            current_board=serialize_board(current_board),
            status=status,
        )

    async def create_move(
        self,
        game_id: int,
        row: int,
        col: int,
        value: int,
        is_valid: bool,
    ):
        await self.get_game(game_id)
        return await self.repository.create_move(
            game_id=game_id,
            row=row,
            col=col,
            value=value,
            is_valid=is_valid,
        )

    async def make_move(
        self,
        game_id: int,
        row: int,
        col: int,
        value: int,
    ) -> GameMoveResponse:
        game = await self.get_game(game_id)

        initial_board = deserialize_board(game.initial_board)
        current_board = deserialize_board(game.current_board)
        solution = deserialize_board(game.solution)

        current_status = str(game.status.value if hasattr(game.status, "value") else game.status)

        if current_status == "solved":
            raise HTTPException(status_code=400, detail="Игра уже решена")

        if initial_board[row][col] != 0:
            raise HTTPException(
                status_code=400,
                detail="Эта клетка является фиксированной и не может быть изменена",
            )

        is_valid = solution[row][col] == value
        current_board[row][col] = value

        new_status = "in_progress"
        message = "Ход сохранён"

        if current_board == solution:
            new_status = "solved"
            message = "Поздравляем! Судоку решено"
        elif value == 0:
            message = "Клетка очищена"
        elif not is_valid:
            message = "Ход сохранён, но число неверное"
        else:
            message = "Число введено верно"

        await self.repository.update_current_board(
            game=game,
            current_board=serialize_board(current_board),
            status=new_status,
        )

        await self.repository.create_move(
            game_id=game.id,
            row=row,
            col=col,
            value=value,
            is_valid=is_valid,
        )

        return GameMoveResponse(
            game_id=game.id,
            row=row,
            col=col,
            value=value,
            is_valid=is_valid,
            status=new_status,
            current_board=current_board,
            message=message,
        )

    async def check_game(self, game_id: int) -> GameCheckResponse:
        game = await self.get_game(game_id)
        current_board = deserialize_board(game.current_board)
        solution = deserialize_board(game.solution)

        validation_result = SudokuService.validate_board(current_board)
        solved = current_board == solution
        status = "solved" if solved else str(game.status.value if hasattr(game.status, "value") else game.status)

        if solved:
            message = "Судоку решено правильно"
        elif validation_result.valid:
            message = "Текущее состояние поля корректно, но игра ещё не завершена"
        else:
            message = validation_result.message

        return GameCheckResponse(
            valid=validation_result.valid,
            solved=solved,
            status=status,
            message=message,
            current_board=current_board,
        )

    async def solve_game(self, game_id: int) -> GamePublicDetailResponse:
        game = await self.get_game(game_id)
        solution = deserialize_board(game.solution)

        updated_game = await self.repository.update_current_board(
            game=game,
            current_board=serialize_board(solution),
            status="solved",
        )
        return self.build_game_public_response(updated_game)

    async def check_cell(
        self,
        game_id: int,
        row: int,
        col: int,
    ) -> CellCheckResponse:
        game = await self.get_game(game_id)

        initial_board = deserialize_board(game.initial_board)
        current_board = deserialize_board(game.current_board)
        solution = deserialize_board(game.solution)

        if initial_board[row][col] != 0:
            return CellCheckResponse(
                row=row,
                col=col,
                value=current_board[row][col],
                checked=True,
                is_correct=True,
                message="Это исходная клетка, она уже задана верно",
            )

        value = current_board[row][col]

        if value == 0:
            return CellCheckResponse(
                row=row,
                col=col,
                value=value,
                checked=False,
                is_correct=False,
                message="Клетка пока пустая",
            )

        is_correct = solution[row][col] == value

        return CellCheckResponse(
            row=row,
            col=col,
            value=value,
            checked=True,
            is_correct=is_correct,
            message="Число верное" if is_correct else "Число неверное",
        )

    @staticmethod
    def build_game_public_response(game) -> GamePublicDetailResponse:
        return GamePublicDetailResponse(
            id=game.id,
            initial_board=deserialize_board(game.initial_board),
            current_board=deserialize_board(game.current_board),
            difficulty=game.difficulty,
            status=str(game.status.value if hasattr(game.status, "value") else game.status),
            created_at=game.created_at,
            updated_at=game.updated_at,
        )