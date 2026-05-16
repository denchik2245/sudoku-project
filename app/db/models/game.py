from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class GameStatus(str, PyEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    SOLVED = "solved"
    FAILED = "failed"


class SudokuGame(Base):
    __tablename__ = "sudoku_games"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    initial_board: Mapped[str] = mapped_column(Text, nullable=False)
    current_board: Mapped[str] = mapped_column(Text, nullable=False)
    solution: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[GameStatus] = mapped_column(
        Enum(GameStatus),
        default=GameStatus.NEW,
        nullable=False,
    )
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

    moves = relationship(
        "SudokuMove",
        back_populates="game",
        cascade="all, delete-orphan",
    )