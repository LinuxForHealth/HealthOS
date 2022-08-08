"""
detect.py
Provides functions pertaining to message format detection and validation.
"""
import json
import logging
from enum import Enum
from typing import Dict, Optional

import hl7
from fhir.resources import construct_fhir_element
from hl7 import ParseException
from linuxforhealth.x12.io import X12ModelReader
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class ContentTypeError(Exception):
    """
    Raised when a message has an invalid or unsupported content type.
    """

    pass


class DataValidationError(Exception):
    """
    Raised when a data message contains validation errors.
    """

    pass


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
    :raises: ContentTypeError if the content type cannot be determined
    """
    if input_message is None or len(input_message) < 3:
        msg = "input message is less than three characters"
        logger.error(msg)
        raise ContentTypeError(msg)

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
        raise ContentTypeError(msg)

    return content_type


def validate_message(input_message: str, content_type: Optional[ContentType] = None):
    """
    Validates an input message based on it's detected content type.
    :param input_message: The input message to validate
    :param content_type: The content type of the message. If not provided, the content type will be detected.
    :raises: ContentTypeError if the content type is unsupported or invalid.
    :raises: DataValidationError if the content type cannot be detected, or if the message is invalid.
    """
    if content_type is None:
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
    # aggregate exception handling for the 3rd party model libraries
    # ValidationError is a catch-all for Pydantic based models (fhir, x12)
    # ParseException is raised by the hl7 library
    # KeyError and AttributeError are additional exceptions which may be raised by x12
    except (ValidationError, ParseException, KeyError, AttributeError) as ex:
        logger.error(f"Unable to load {content_type} due to {ex}")
        raise DataValidationError(str(ex))

    return content_type
