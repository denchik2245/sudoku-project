import json


def serialize_board(board: list[list[int]]) -> str:
    return json.dumps(board)


def deserialize_board(board_data: str) -> list[list[int]]:
    return json.loads(board_data)
