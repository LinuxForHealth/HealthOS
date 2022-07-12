"""
detect.py
Provides functions pertaining to message format detection and validation.
"""
from enum import Enum
import logging
import json
from typing import Dict
from linuxforhealth.x12.io import X12ModelReader
from fhir.resources import construct_fhir_element
import hl7

logger = logging.getLogger(__name__)


class ContentType(str, Enum):
    """
    Supported Content Types for the RestEndpoint
    """

    ASC_X12 = "application/EDI-X12"
    # TODO: support commented out content types
    # CDA_XML = "application/cda+xml"
    # DICOM = "application/dicom"
    # DICOM_JSON = "application/dicom+json"
    # DICOM_XML = "application/dicom+xml"
    FHIR_JSON = "application/fhir+json"
    # FHIR_XML = "application/fhir+xml"
    HL7_TEXT = "text/hl7v2"
    # HL7_XML = "application/hl7v2+xml"]


def detect_content_type(input_message: str) -> ContentType:
    """
    Returns the content type of the input message.
    If the content type cannot be determined, a ValueError is raised.
    :param input_message: The message to analyze
    :return: ContentType
    :raises: ValueError if the content type cannot be determined
    """
    if input_message is None or len(input_message) < 3:
        msg = "input message is less than three characters"
        logger.error(msg)
        raise ValueError(msg)

    first_chars = input_message.lstrip()[0:3].lower()
    content_type: ContentType | None = None

    if first_chars.startswith("{"):
        json_data: Dict = json.loads(input_message)
        if json_data.get("resourceType"):
            content_type = ContentType.FHIR_JSON
    elif first_chars.startswith("isa"):
        content_type = ContentType.ASC_X12
    elif first_chars.startswith("msh"):
        content_type = ContentType.HL7_TEXT

    if content_type is None:
        msg = "unable to determine content type"
        logger.error(msg)
        raise ValueError(msg)

    return content_type


def validate_message(input_message) -> ContentType:
    """
    Validates an input message based on it's detected content type.
    :param input_message: The input message to validate
    :returns: The content type of the validated message
    :raises: ValueError if the content type cannot be detected, or if the message is invalid.
    """
    content_type: ContentType = detect_content_type(input_message)

    try:
        match content_type:
            case ContentType.ASC_X12:
                with X12ModelReader(input_message) as r:
                    for _ in r.models():
                        pass

            case ContentType.FHIR_JSON:
                fhir_data = json.loads(input_message)
                resource_type = fhir_data.get("resourceType")
                construct_fhir_element(resource_type, fhir_data)

            case ContentType.HL7_TEXT:
                hl7.parse(input_message)
    except Exception as ex:
        logger.error(f"Unable to load {content_type} due to {ex}")
        raise ValueError(f"Unable to load {content_type}")

    return content_type
