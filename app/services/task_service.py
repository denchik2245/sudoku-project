import json
from typing import Any

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskResponse
from app.services.broker_service import BrokerService


class TaskService:
    def __init__(self, session: AsyncSession):
        self.repository = TaskRepository(session)
        self.broker = BrokerService()

    async def create_task(
        self,
        task_type: str,
        input_data: dict[str, Any] | None = None,
    ):
        serialized_input = json.dumps(input_data) if input_data is not None else None

        task = await self.repository.create_task(
            task_type=task_type,
            input_data=serialized_input,
        )

        message = {
            "task_id": task.id,
            "task_type": task_type,
            "input_data": input_data or {},
        }

        await self.broker.publish_message(message)
        return task

    async def get_task(self, task_id: int):
        task = await self.repository.get_task_by_id(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    async def update_task(
        self,
        task_id: int,
        status: str | None = None,
        result_data: dict[str, Any] | None = None,
    ):
        task = await self.get_task(task_id)
        serialized_result = json.dumps(result_data) if result_data is not None else None
        return await self.repository.update_task(
            task=task,
            status=status,
            result_data=serialized_result,
        )

    @staticmethod
    def build_task_response(task) -> TaskResponse:
        return TaskResponse(
            id=task.id,
            task_type=str(task.task_type.value if hasattr(task.task_type, "value") else task.task_type),
            status=str(task.status.value if hasattr(task.status, "value") else task.status),
            input_data=json.loads(task.input_data) if task.input_data else None,
            result_data=json.loads(task.result_data) if task.result_data else None,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
