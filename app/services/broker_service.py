import json

import aio_pika

from app.core.config import settings


class BrokerService:
    def __init__(self):
        self.rabbitmq_url = settings.rabbitmq_url
        self.queue_name = settings.rabbitmq_queue

    async def publish_message(self, message: dict) -> None:
        connection = await aio_pika.connect_robust(self.rabbitmq_url)

        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.queue_name, durable=True)

            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode("utf-8"),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=queue.name,
            )
