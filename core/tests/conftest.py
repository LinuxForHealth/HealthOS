import os
from typing import Callable, List
from unittest.mock import AsyncMock

import nats
import pytest
import yaml
from aiokafka import ConsumerRecord
from nats import NATS
from nats.js import JetStreamContext, JetStreamManager

from linuxforhealth.healthos.core.config import CoreServiceConfig
from tests.support import resources_directory

from .support import AsyncIterator


@pytest.fixture
def resources_path() -> str:
    """returns the path to the test resources directory"""
    return resources_directory


@pytest.fixture
def mock_kafka_consumer() -> Callable:
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


@pytest.fixture
def mock_nats():
    """
    NATS Fixture provides AsyncMocks for:
    - Nats Client
    - Jetstream
    - Jetstream Manager
    :return: NATS fixture
    """
    mock_nats = AsyncMock(spec=nats)
    mock_nats_client = AsyncMock(spec=NATS)
    mock_nats_js_mgr = AsyncMock(spec=JetStreamManager)
    mock_nats_js = AsyncMock(spec=JetStreamContext)

    mock_nats.connect.return_value = mock_nats_client
    mock_nats_client.jetstream.return_value = mock_nats_js
    mock_nats_client.jsm.return_value = mock_nats_js_mgr

    return mock_nats


@pytest.fixture
def core_configuration(resources_path) -> Callable:
    """
    Returns a function used to load a CoreConfiguration from "test" resources.
    The function accepts a simple argument, the configuration file name.

    :param resources_path: The fixture representing the path to the resources directory.
    :return: function used to load HealthOS Core Configuration model
    """

    def _load_core_configuration(file_name: str) -> CoreServiceConfig:
        """
        Loads a core configuration from file.

        :param file_name: The configuration file name.
        :return: CoreServiceConfig
        """
        config_path = os.path.join(resources_path, "service-config", file_name)
        with open(config_path) as fp:
            core_data = yaml.safe_load(fp)

        return CoreServiceConfig(**core_data)

    return _load_core_configuration
