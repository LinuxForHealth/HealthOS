"""
test_rest_connector.py
"""
from unittest.mock import AsyncMock

import pytest

from linuxforhealth.healthos.core.connector.rest import (HTTPException,
                                                         NoStreamResponseError,
                                                         RestEndpointRequest,
                                                         RestEndpointResponse,
                                                         endpoint_template)


@pytest.fixture
def request_model():
    """Request model fixture used in tests"""
    return RestEndpointRequest(data="valid-hl7v2-data-payload")


@pytest.mark.asyncio
async def test_endpoint_template(monkeypatch, publish_model, request_model):
    """
    Tests the Rest Endpoint Template when no errors occur.

    :param monkeypatch: The pytest monkeypatch fixture.
    :param publish_model: The publish model fixture used as a return type for the process_data function.
    :param request_model: The request model fixture used to stand-in for the initial request.
    :return:
    """
    mock_process_data = AsyncMock()
    mock_process_data.return_value = publish_model

    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.rest.process_data", mock_process_data
    )

    endpoint_response: RestEndpointResponse = await endpoint_template(request_model)
    assert endpoint_response.data_id == str(publish_model.data_id)
    assert endpoint_response.content_type == publish_model.content_type
    assert endpoint_response.status == "received"


@pytest.mark.asyncio
async def test_endpoint_template_value_error(monkeypatch, publish_model, request_model):
    """
    Tests the Rest Endpoint Template when a value error occurs.

    :param monkeypatch: The pytest monkeypatch fixture.
    :param publish_model: The publish model fixture used as a return type for the process_data function.
    :param request_model: The request model fixture used to stand-in for the initial request.
    :return:
    """
    mock_process_data = AsyncMock()
    mock_process_data.side_effect = ValueError("Invalid data")

    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.rest.process_data", mock_process_data
    )

    endpoint_response: RestEndpointResponse = await endpoint_template(request_model)
    assert endpoint_response.data_id is not None
    assert endpoint_response.status == "failed"


@pytest.mark.asyncio
async def test_endpoint_template_internal_error(
    monkeypatch, publish_model, request_model
):
    """
    Tests the Rest Endpoint Template when an internal error occurs.

    :param monkeypatch: The pytest monkeypatch fixture.
    :param publish_model: The publish model fixture used as a return type for the process_data function.
    :param request_model: The request model fixture used to stand-in for the initial request.
    :return:
    """
    mock_process_data = AsyncMock()
    mock_process_data.side_effect = NoStreamResponseError()

    monkeypatch.setattr(
        "linuxforhealth.healthos.core.connector.rest.process_data", mock_process_data
    )

    with pytest.raises(HTTPException) as e:
        await endpoint_template(request_model)
