from app.sudoku.utils import Board, get_box, get_column, get_row


class SudokuValidator:
    @staticmethod
    def is_board_shape_valid(board: Board) -> bool:
        if len(board) != 9:
            return False
        return all(len(row) == 9 for row in board)

    @staticmethod
    def is_value_range_valid(board: Board) -> bool:
        for row in board:
            for cell in row:
                if not isinstance(cell, int):
                    return False
                if cell < 0 or cell > 9:
                    return False
        return True

    @staticmethod
    def _is_unit_valid(values: list[int]) -> bool:
        filtered = [value for value in values if value != 0]
        return len(filtered) == len(set(filtered))

    @classmethod
    def is_rows_valid(cls, board: Board) -> bool:
        for row in range(9):
            if not cls._is_unit_valid(get_row(board, row)):
                return False
        return True

    @classmethod
    def is_columns_valid(cls, board: Board) -> bool:
        for col in range(9):
            if not cls._is_unit_valid(get_column(board, col)):
                return False
        return True

    @classmethod
    def is_boxes_valid(cls, board: Board) -> bool:
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                if not cls._is_unit_valid(get_box(board, row, col)):
                    return False
        return True

    @classmethod
    def is_board_valid(cls, board: Board) -> bool:
        return (
            cls.is_board_shape_valid(board)
            and cls.is_value_range_valid(board)
            and cls.is_rows_valid(board)
            and cls.is_columns_valid(board)
            and cls.is_boxes_valid(board)
        )

    @staticmethod
    def can_place(board: Board, row: int, col: int, value: int) -> bool:
        if value == 0:
            return True

        for c in range(9):
            if c != col and board[row][c] == value:
                return False

        for r in range(9):
            if r != row and board[r][col] == value:
                return False

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r != row or c != col) and board[r][c] == value:
                    return False

        return True
