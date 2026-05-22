from app.schemas.sudoku import SudokuSolveResponse, SudokuValidateResponse
from app.services.cache_service import CacheService
from app.sudoku.generator import SudokuGenerator
from app.sudoku.solver import SudokuSolver
from app.sudoku.validator import SudokuValidator
import json


class SudokuService:
    @staticmethod
    def validate_board(board: list[list[int]]) -> SudokuValidateResponse:
        if not SudokuValidator.is_board_shape_valid(board):
            return SudokuValidateResponse(
                valid=False,
                message="Поле должно быть размером 9x9",
            )

        if not SudokuValidator.is_value_range_valid(board):
            return SudokuValidateResponse(
                valid=False,
                message="Поле должно содержать только целые числа от 0 до 9",
            )

        if not SudokuValidator.is_board_valid(board):
            return SudokuValidateResponse(
                valid=False,
                message="Поле нарушает правила судоку",
            )

        return SudokuValidateResponse(
            valid=True,
            message="Поле заполнено корректно",
        )

    @staticmethod
    async def solve_board(board: list[list[int]]) -> SudokuSolveResponse:
        if not SudokuValidator.is_board_shape_valid(board):
            return SudokuSolveResponse(
                solved=False,
                solution=None,
                message="Поле должно быть размером 9x9",
            )

        if not SudokuValidator.is_value_range_valid(board):
            return SudokuSolveResponse(
                solved=False,
                solution=None,
                message="Поле должно содержать только целые числа от 0 до 9",
            )

        if not SudokuValidator.is_board_valid(board):
            return SudokuSolveResponse(
                solved=False,
                solution=None,
                message="Поле нарушает правила судоку",
            )

        cache_service = CacheService()
        cache_key = cache_service.make_solve_key(board)

        cached_result = await cache_service.get(cache_key)
        if cached_result:
            data = json.loads(cached_result)
            await cache_service.close()
            return SudokuSolveResponse(
                solved=data["solved"],
                solution=data["solution"],
                message="Судоку решено успешно (из кэша)",
            )

        solution = SudokuSolver.solve(board)
        if solution is None:
            await cache_service.close()
            return SudokuSolveResponse(
                solved=False,
                solution=None,
                message="Не удалось решить судоку",
            )

        response_data = {
            "solved": True,
            "solution": solution,
        }
        await cache_service.set(cache_key, response_data, expire=600)
        await cache_service.close()

        return SudokuSolveResponse(
            solved=True,
            solution=solution,
            message="Судоку решено успешно",
        )

    @staticmethod
    async def generate_board(difficulty: str = "easy") -> dict:
        cache_service = CacheService()
        cache_key = cache_service.make_generate_key(difficulty)

        cached_result = await cache_service.get(cache_key)
        if cached_result:
            data = json.loads(cached_result)
            await cache_service.close()
            data["message"] = "Поле получено из кэша"
            return data

        puzzle, solution = SudokuGenerator.generate(difficulty=difficulty)

        response_data = {
            "puzzle": puzzle,
            "solution": solution,
            "difficulty": difficulty,
        }

        await cache_service.set(cache_key, response_data, expire=300)
        await cache_service.close()

        return response_data
