from app.sudoku.utils import Board, deep_copy_board, find_empty_cell, shuffle_numbers
from app.sudoku.validator import SudokuValidator


class SudokuSolver:
    @classmethod
    def solve(cls, board: Board) -> Board | None:
        if not SudokuValidator.is_board_valid(board):
            return None

        board_copy = deep_copy_board(board)

        if cls._solve_backtracking(board_copy):
            return board_copy

        return None

    @classmethod
    def _solve_backtracking(cls, board: Board) -> bool:
        empty_cell = find_empty_cell(board)
        if empty_cell is None:
            return True

        row, col = empty_cell

        for value in range(1, 10):
            if SudokuValidator.can_place(board, row, col, value):
                board[row][col] = value

                if cls._solve_backtracking(board):
                    return True

                board[row][col] = 0

        return False

    @classmethod
    def fill_board_randomly(cls, board: Board) -> bool:
        empty_cell = find_empty_cell(board)
        if empty_cell is None:
            return True

        row, col = empty_cell

        for value in shuffle_numbers():
            if SudokuValidator.can_place(board, row, col, value):
                board[row][col] = value

                if cls.fill_board_randomly(board):
                    return True

                board[row][col] = 0

        return False
