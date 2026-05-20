import asyncio
import json

import aio_pika

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.services.task_service import TaskService
from app.services.sudoku_service import SudokuService


async def process_task(message_body: dict) -> None:
    task_id = message_body["task_id"]
    task_type = message_body["task_type"]
    input_data = message_body.get("input_data", {})

    async with AsyncSessionLocal() as session:
        task_service = TaskService(session)

        await task_service.update_task(task_id=task_id, status="processing")

        try:
            if task_type == "generate":
                difficulty = input_data.get("difficulty", "easy")
                result = await SudokuService.generate_board(difficulty)

            elif task_type == "solve":
                board = input_data.get("board")
                solve_result = await SudokuService.solve_board(board)
                result = {
                    "solved": solve_result.solved,
                    "solution": solve_result.solution,
                    "message": solve_result.message,
                }

            else:
                result = {
                    "error": f"Неподдерживаемый тип задачи: {task_type}"
                }
                await task_service.update_task(
                    task_id=task_id,
                    status="failed",
                    result_data=result,
                )
                return

            await task_service.update_task(
                task_id=task_id,
                status="done",
                result_data=result,
            )

        except Exception as exc:
            await task_service.update_task(
                task_id=task_id,
                status="failed",
                result_data={"error": f"Ошибка обработки задачи: {str(exc)}"},
            )


async def consume() -> None:
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(settings.rabbitmq_queue, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = json.loads(message.body.decode("utf-8"))
                    await process_task(body)


def main() -> None:
    asyncio.run(consume())


if __name__ == "__main__":
    main()
