"""
test_processor.py

Tests the common functions and routines used to process connector data.
"""
import os
import uuid
from unittest.mock import AsyncMock

import pytest
from nats.js import JetStreamContext
from nats.js.errors import NoStreamResponseError

from linuxforhealth.healthos.core.connector.processor import (
    PublishDataModel,
    get_core_configuration,
    process_data,
    ContentTypeError
)


@pytest.fixture
def sample_data_path(resources_path) -> str:
    """Returns the path to the test resources sample-data directory"""
    return os.path.join(resources_path, "sample-data")


def test_publish_data_model():
    """
    Validates the PublishDataModel does not raise an issue with no data.
    """
    m = PublishDataModel(data="a sample message", content_type="text/hl7v2")
    assert isinstance(m.data_id, uuid.UUID)
    assert m.data == "a sample message"
    assert m.content_type == "text/hl7v2"


@pytest.mark.parametrize(
    "file_name,content_type",
    [
        ("270.x12", "application/EDI-X12"),
        ("adt_a01_26.hl7", "text/hl7v2"),
        ("fhir-us-core-patient.json", "application/fhir+json"),
    ],
)
@pytest.mark.asyncio
async def test_process_data(
    monkeypatch, core_configuration, sample_data_path, file_name, content_type
):
    """
    Validates process_data when no errors occur

    :param monkeypatch: The pytest monkeypatch fixture
    :param core_configuration: Fixture used to load a HealthOS Core Configuration Model
    :param sample_data_path: The path to the sample-data directory
    :param file_name: The file name containing the test message
    :param content_type: The message's expected content type
    """
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.processor.get_core_configuration",
        lambda:  core_configuration("core-service.yml"),
    )

    mock_js_client = AsyncMock(spec=JetStreamContext)
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.nats.get_jetstream_core_client",
        lambda: mock_js_client,
    )

    file_path = os.path.join(sample_data_path, file_name)
    with open(file_path, "r") as f:
        message = "".join(f.readlines())

    actual_model = await process_data(message)
    assert actual_model.content_type == content_type
    assert actual_model.data_id is not None
    assert actual_model.data == message

    assert mock_js_client.publish.call_count == 1


@pytest.mark.parametrize("invalid_file_name", ["demographics.csv", "invalid-270.x12"])
@pytest.mark.asyncio
async def test_process_data_invalid_content_type(
    monkeypatch, core_configuration, sample_data_path: str, invalid_file_name: str
):
    """
    Validates process_data when the message content type is invalid

    :param monkeypatch: The pytest monkeypatch fixture
    :param core_configuration: Fixture used to load a HealthOS Core Configuration Model
    :param sample_data_path: The path to the sample-data directory
    :param invalid_file_name: The file name containing the test message
    """
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.processor.get_core_configuration",
        lambda: core_configuration("core-service.yml"),
    )

    mock_js_client = AsyncMock(spec=JetStreamContext)
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.nats.get_jetstream_core_client",
        lambda: mock_js_client,
    )

    invalid_path = os.path.join(sample_data_path, invalid_file_name)
    with open(invalid_path, "r") as f:
        invalid_message = "".join(f.readlines())

    publish_model: PublishDataModel = await process_data(invalid_message)
    assert publish_model.error is not None
    assert mock_js_client.publish.call_count == 1


@pytest.mark.asyncio
async def test_process_data_stream_error(
    monkeypatch, core_configuration, sample_data_path
):
    """
    Validates process_data raises a NoStreamResponseError when a NATs processing issue occurs
    """
    config = core_configuration("core-service.yml")
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.processor.get_core_configuration",
        lambda: config,
    )

    mock_js_client = AsyncMock(spec=JetStreamContext)
    mock_js_client.publish.side_effect = NoStreamResponseError()
    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.nats.get_jetstream_core_client",
        lambda: mock_js_client,
    )

    file_path = os.path.join(sample_data_path, "270.x12")
    with open(file_path, "r") as f:
        message = "".join(f.readlines())

    with pytest.raises(NoStreamResponseError):
        await process_data(message)
