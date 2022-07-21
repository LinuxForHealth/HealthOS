"""
kafka.py

Implements Kafka connectors for consuming and publishing data.
"""
import asyncio
import logging
from typing import List

from aiokafka import AIOKafkaConsumer

from ..config import ConnectorConfig
from .processor import PublishDataModel, process_data

kafka_consumer_connectors: List[AIOKafkaConsumer] | None = None

logger = logging.getLogger(__name__)


async def consume_message(kafka_consumer: AIOKafkaConsumer):
    """
    Consumes messages from a Kafka Consumer

    :param kafka_consumer: the aiokafka consumer
    """
    async for msg in kafka_consumer:
        try:
            data_message = msg.value.decode("utf-8")
            publish_model: PublishDataModel = await process_data(data_message)

            logger.debug(
                f"published data to NATS data_id = {publish_model.data_id} "
                + f"content_type = {publish_model.content_type}"
            )
        except ValueError as ve:
            logger.warning(f"Invalid message. Exception {ve}")


async def consume_message_task(kafka_consumer: AIOKafkaConsumer):
    """
    AsyncIO task used to consume messages from a Kafka Consumer.

    :param kafka_consumer: The aiokafka consumer.
    """
    logger.debug(
        f"Running Kafka Consumer Task, subscribed to {kafka_consumer.subscription()}"
    )
    while True:
        await consume_message(kafka_consumer)


async def create_kafka_consumer_connector(
    inbound_kafka_consumers: List[ConnectorConfig],
):
    """
    Creates a Kafka Consumer Connector and starts it with the specified configuration.

    :param inbound_kafka_consumers: The kafka consumer configuration
    """
    global kafka_consumer_connectors
    kafka_consumer_connectors = []

    try:
        for i, k in enumerate(inbound_kafka_consumers):
            topics = k.config.topics
            configuration_data = k.config.dict(exclude={"type", "subjects", "topics"})
            c = AIOKafkaConsumer(*topics, **configuration_data)
            await c.start()
            logger.info(f"Started Kafka consumer for {k.config.bootstrap_servers}")
            kafka_consumer_connectors.append(c)
            consumer_task = asyncio.get_running_loop().create_task(
                consume_message_task(c), name=f"healthos_kafka_consumer_{i}"
            )
            logger.info(
                f"Created task to consume Kafka messages {consumer_task.get_name()}"
            )

    except Exception as ex:
        logger.error(f"Unable to start Kafka Consumer. Error {ex}")
        raise


def get_kafka_consumer_connectors() -> List[AIOKafkaConsumer]:
    """Returns the Kafka Consumer Connectors"""
    global kafka_consumer_connectors
    return kafka_consumer_connectors or []
