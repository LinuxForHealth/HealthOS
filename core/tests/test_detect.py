"""
test_detect
"""
import os

import pytest

from linuxforhealth.healthos.core.detect import (ContentType,
                                                 detect_content_type,
                                                 validate_message)


@pytest.fixture
def sample_data_path(resources_path) -> str:
    return os.path.join(resources_path, "sample-data")


@pytest.mark.parametrize(
    "file_name, content_type",
    [
        ("270.x12", ContentType.ASC_X12),
        ("adt_a01_26.hl7", ContentType.HL7_TEXT),
        ("fhir-us-core-patient.json", ContentType.FHIR_JSON),
    ],
)
def test_detect_content_type(
    sample_data_path: str, file_name: str, content_type: ContentType
):
    """
    Validates detect_content_type when no errors occur.

    :param sample_data_path: The path to the sample data directory.
    :param file_name:  The file name, within the sample data directory, to test.
    :param content_type: The expected ContentType
    """
    file_path = os.path.join(sample_data_path, file_name)
    with open(file_path) as f:
        input_message = "".join(f.readlines())

    actual_content_type = detect_content_type(input_message)
    assert content_type == actual_content_type


def test_detect_content_type_exception(sample_data_path: str):
    """
    Validates detect_content_type raises an exception when appropriate.
    :param sample_data_path: The sample data path
    """
    file_path = os.path.join(sample_data_path, "demographics.csv")
    with open(file_path) as f:
        input_message = "".join(f.readlines())

    with pytest.raises(ValueError):
        detect_content_type(input_message)


@pytest.mark.parametrize(
    "file_name, content_type",
    [
        ("270.x12", ContentType.ASC_X12),
        ("adt_a01_26.hl7", ContentType.HL7_TEXT),
        ("fhir-us-core-patient.json", ContentType.FHIR_JSON),
    ],
)
def test_validate_message(
    sample_data_path: str, file_name: str, content_type: ContentType
):
    """
    Validates that validate_message does not raise an exception for valid input messages.

    :param sample_data_path: The path to the sample data directory.
    :param file_name: The file name within the sample data directory to test.
    :param content_type: The expected content type
    """
    file_path = os.path.join(sample_data_path, file_name)
    with open(file_path) as f:
        input_message = "".join(f.readlines())

    actual_content_type = validate_message(input_message)
    assert content_type == actual_content_type


def test_validate_message_exception(sample_data_path: str):
    """
    Validates validate_message raises an exception when appropriate.
    :param sample_data_path: The sample data path
    """
    file_path = os.path.join(sample_data_path, "invalid-270.x12")
    with open(file_path) as f:
        input_message = "".join(f.readlines())

    with pytest.raises(ValueError):
        validate_message(input_message)
