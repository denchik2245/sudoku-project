from fastapi import APIRouter

from app.schemas.sudoku import (
    SudokuBoardRequest,
    SudokuGenerateRequest,
    SudokuGenerateResponse,
    SudokuSolveRequest,
    SudokuSolveResponse,
    SudokuValidateResponse,
)
from app.services.sudoku_service import SudokuService

router = APIRouter(prefix="/sudoku", tags=["Судоку"])


@router.post("/validate", response_model=SudokuValidateResponse)
async def validate_sudoku(payload: SudokuBoardRequest) -> SudokuValidateResponse:
    return SudokuService.validate_board(payload.board)


@router.post("/solve", response_model=SudokuSolveResponse)
async def solve_sudoku(payload: SudokuSolveRequest) -> SudokuSolveResponse:
    return await SudokuService.solve_board(payload.board)


@router.post("/generate", response_model=SudokuGenerateResponse)
async def generate_sudoku(payload: SudokuGenerateRequest) -> SudokuGenerateResponse:
    data = await SudokuService.generate_board(payload.difficulty)
    return SudokuGenerateResponse(
        puzzle=data["puzzle"],
        solution=data["solution"],
        difficulty=data["difficulty"],
    )
