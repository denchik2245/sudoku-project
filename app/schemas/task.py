from datetime import datetime
from typing import Any

from pydantic import BaseModel


class TaskGenerateRequest(BaseModel):
    difficulty: str = "easy"


class TaskSolveRequest(BaseModel):
    board: list[list[int]]


class TaskResponse(BaseModel):
    id: int
    task_type: str
    status: str
    input_data: dict[str, Any] | None = None
    result_data: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
