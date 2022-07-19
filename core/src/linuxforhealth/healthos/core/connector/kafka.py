"""
kafka.py

Implements Kafka connectors for consuming and publishing data.
"""
import logging
from typing import Dict

from aiokafka import AIOKafkaConsumer

from .processor import PublishDataModel, process_data

kafka_consumer_connector: AIOKafkaConsumer

logger = logging.getLogger(__name__)


async def start_kafka_consumer_connector(consumer_config: Dict):
    """
    Creates a Kafka Consumer Connector and starts it with the specified configuration.

    :param consumer_config: The kafka consumer configuration
    """
    global kafka_consumer_connector
    try:
        kafka_consumer_connector = AIOKafkaConsumer(**consumer_config)
    except Exception as ex:
        logger.error(f"Unable to create Kafka Consumer. Error {ex}")
        raise

    try:
        await kafka_consumer_connector.start()
    except Exception as ex:
        logger.error(f"Unable to start Kafka Consumer Connector. Error {ex}")
        raise

    async for msg in kafka_consumer_connector:
        try:
            publish_model: PublishDataModel = process_data(msg)
        except ValueError as ve:
            logger.warning(f"Invalid message. Exception {ve}")
