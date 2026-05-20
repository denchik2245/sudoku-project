from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TaskType(str, PyEnum):
    GENERATE = "generate"
    SOLVE = "solve"


class TaskStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


class SudokuTask(Base):
    __tablename__ = "sudoku_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_type: Mapped[TaskType] = mapped_column(
        Enum(TaskType),
        nullable=False,
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False,
    )
    input_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
