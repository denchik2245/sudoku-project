from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.task import SudokuTask


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(
        self,
        task_type: str,
        input_data: str | None = None,
        status: str = "pending",
    ) -> SudokuTask:
        task = SudokuTask(
            task_type=task_type,
            input_data=input_data,
            status=status,
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_task_by_id(self, task_id: int) -> SudokuTask | None:
        result = await self.session.execute(
            select(SudokuTask).where(SudokuTask.id == task_id)
        )
        return result.scalar_one_or_none()

    async def update_task(
        self,
        task: SudokuTask,
        status: str | None = None,
        result_data: str | None = None,
    ) -> SudokuTask:
        if status is not None:
            task.status = status

        if result_data is not None:
            task.result_data = result_data

        await self.session.commit()
        await self.session.refresh(task)
        return task
