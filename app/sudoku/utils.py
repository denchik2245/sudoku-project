import copy
import random


Board = list[list[int]]


def deep_copy_board(board: Board) -> Board:
    return copy.deepcopy(board)


def empty_board() -> Board:
    return [[0 for _ in range(9)] for _ in range(9)]


def find_empty_cell(board: Board) -> tuple[int, int] | None:
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None


def get_row(board: Board, row: int) -> list[int]:
    return board[row]


def get_column(board: Board, col: int) -> list[int]:
    return [board[row][col] for row in range(9)]


def get_box(board: Board, row: int, col: int) -> list[int]:
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    box = []
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            box.append(board[r][c])
    return box


def shuffle_numbers() -> list[int]:
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    return numbers
