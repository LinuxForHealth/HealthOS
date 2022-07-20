"""
test_nats_core_client.py

Tests the HealthOS NATS Core Client.
"""
import pytest

from linuxforhealth.healthos.core.connector.nats import (
    create_jetstream_core_client, get_jetstream_core_client)


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
