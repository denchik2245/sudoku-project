from app.sudoku.solver import SudokuSolver
from app.sudoku.utils import Board, deep_copy_board, empty_board

import random


class SudokuGenerator:
    DIFFICULTY_REMOVALS = {
        "easy": 35,
        "medium": 45,
        "hard": 55,
    }

    @classmethod
    def generate(cls, difficulty: str = "easy") -> tuple[Board, Board]:
        solved_board = empty_board()
        SudokuSolver.fill_board_randomly(solved_board)

        puzzle_board = deep_copy_board(solved_board)
        cls._remove_cells(puzzle_board, difficulty)

        return puzzle_board, solved_board

    @classmethod
    def _remove_cells(cls, board: Board, difficulty: str) -> None:
        removals = cls.DIFFICULTY_REMOVALS.get(difficulty, 35)
        removed = 0

        while removed < removals:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if board[row][col] != 0:
                board[row][col] = 0
                removed += 1
