"""
test_nats_core_client.py

Tests the HealthOS NATS Core Client.
"""
from unittest.mock import AsyncMock

import pytest
from nats.js.errors import NotFoundError

from linuxforhealth.healthos.core.connector.nats import (
    create_jetstream_core_client,
    get_jetstream_core_client,
)


@pytest.mark.asyncio
async def test_create_jetstream_core_client(monkeypatch, mock_nats):
    """
    Validates create_jetstream_core_clients creates the HealthOS Core NATS client

    :param monkeypatch: The pytest monkeypatch fixture
    :param mock_nats: The mock nats fixture
    :return:
    """
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.nats.jetstream_core_client", None
    )
    monkeypatch.setattr("linuxforhealth.healthos.core.connector.nats.nats", mock_nats)

    core_client = get_jetstream_core_client()
    assert core_client is None

    await create_jetstream_core_client("nats://localhost:4222", "healthos", "ingress")

    core_client = get_jetstream_core_client()
    assert core_client is not None


@pytest.mark.asyncio
async def test_create_jetstream_core_client_stream_does_not_exist(
    monkeypatch, mock_nats
):
    """
    Validates create_jetstream_core_clients creates a client and a new stream, if the stream does not exist.

    :param monkeypatch: The pytest monkeypatch fixture
    :param mock_nats: The mock nats fixture
    :return:
    """
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.nats.jetstream_core_client", None
    )
    monkeypatch.setattr("linuxforhealth.healthos.core.connector.nats.nats", mock_nats)

    # update mock to raise a NotFoundError to simulate a non-existent stream
    mock_nats_client: AsyncMock = mock_nats.connect.return_value
    mock_jsm: AsyncMock = mock_nats_client.jsm.return_value
    mock_jsm.stream_info.side_effect = NotFoundError()

    core_client = get_jetstream_core_client()
    assert core_client is None

    await create_jetstream_core_client("nats://localhost:4222", "healthos", "ingress")
    assert mock_jsm.add_stream.call_count == 1

    core_client = get_jetstream_core_client()
    assert core_client is not None
