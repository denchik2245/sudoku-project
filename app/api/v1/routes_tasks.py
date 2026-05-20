from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.task import TaskGenerateRequest, TaskResponse, TaskSolveRequest
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Фоновые задачи"])


@router.post("/generate", response_model=TaskResponse)
async def create_generate_task(
    payload: TaskGenerateRequest,
    session: AsyncSession = Depends(get_db),
) -> TaskResponse:
    service = TaskService(session)
    task = await service.create_task(
        task_type="generate",
        input_data={"difficulty": payload.difficulty},
    )
    return service.build_task_response(task)


@router.post("/solve", response_model=TaskResponse)
async def create_solve_task(
    payload: TaskSolveRequest,
    session: AsyncSession = Depends(get_db),
) -> TaskResponse:
    service = TaskService(session)
    task = await service.create_task(
        task_type="solve",
        input_data={"board": payload.board},
    )
    return service.build_task_response(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_db),
) -> TaskResponse:
    service = TaskService(session)
    task = await service.get_task(task_id)
    return service.build_task_response(task)
