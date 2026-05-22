from pydantic import BaseModel, Field


class SudokuBoardRequest(BaseModel):
    board: list[list[int]]


class SudokuSolveRequest(BaseModel):
    board: list[list[int]]


class SudokuValidateResponse(BaseModel):
    valid: bool
    message: str


class SudokuSolveResponse(BaseModel):
    solved: bool
    solution: list[list[int]] | None = None
    message: str


class SudokuGenerateRequest(BaseModel):
    difficulty: str = Field(default="easy", examples=["easy"])


class SudokuGenerateResponse(BaseModel):
    puzzle: list[list[int]]
    solution: list[list[int]]
    difficulty: str
