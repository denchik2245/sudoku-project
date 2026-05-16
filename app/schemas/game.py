from datetime import datetime

from pydantic import BaseModel, Field


class GameCreateRequest(BaseModel):
    difficulty: str = Field(default="easy", examples=["easy"])


class GamePublicDetailResponse(BaseModel):
    id: int
    initial_board: list[list[int]]
    current_board: list[list[int]]
    difficulty: str
    status: str
    created_at: datetime
    updated_at: datetime


class GameMoveRequest(BaseModel):
    row: int = Field(..., ge=0, le=8)
    col: int = Field(..., ge=0, le=8)
    value: int = Field(..., ge=0, le=9)


class GameMoveResponse(BaseModel):
    game_id: int
    row: int
    col: int
    value: int
    is_valid: bool
    status: str
    current_board: list[list[int]]
    message: str


class GameCheckResponse(BaseModel):
    valid: bool
    solved: bool
    status: str
    message: str
    current_board: list[list[int]]


class CellCheckResponse(BaseModel):
    row: int
    col: int
    value: int
    checked: bool
    is_correct: bool
    message: str
