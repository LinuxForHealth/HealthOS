from typing import Callable, List

import pytest
from aiokafka import ConsumerRecord

from tests.support import resources_directory

from .support import AsyncIterator


@pytest.fixture
def resources_path() -> str:
    """returns the path to the test resources directory"""
    return resources_directory


@pytest.fixture
def kafka_consumer() -> Callable:
    """
    Returns a function used to configure an AsyncMock KafkaConsumer with messages.
    The configuration function accepts a single argument, a List[bytes] representing the sample messages which will
    be consumed.
    :return: the configuration function.
    """

    def _create_kafka_consumer(mock_messages: List[bytes]) -> AsyncIterator:
        """
        Creates an AsyncMock Kafka Consumer with a list of binary mock messages

        :param mock_messages: List of messages (bytes)
        """
        consumer_records = []
        for m in mock_messages:
            r = ConsumerRecord(
                topic="healthy-data",
                partition=1,
                offset=0,
                timestamp=0,
                timestamp_type=0,
                key=None,
                value=m,
                checksum=None,
                serialized_key_size=0,
                serialized_value_size=4,
                headers=[],
            )
            consumer_records.append(r)

        kafka_consumer = AsyncIterator(consumer_records)
        return kafka_consumer

    return _create_kafka_consumer
