"""
data.py

Defines common datatypes used within HealthOS components.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from uuid import UUID, uuid4
import datetime


class DataFormat(str, Enum):
    """
    The supported HealthOS data formats
    """

    ASC_X12 = "ASC_X12"
    C_CDA = "C_CDA"
    CUSTOM = "CUSTOM"
    DICOM = "DICOM"
    FHIR_JSON = "FHIR_JSON"
    FHIR_XML = "FHIR_XML"
    HL7_V2 = "HL7_V2"
    HL7_V3 = "HL7_V3"
    OMOP = "OMOP"


class MetaRecord(BaseModel):
    """
    Provides metadata for a HealthOS data record, including the storage URI used to access the source data.
    """

    uuid: UUID = Field(default_factory=uuid4)
    creation_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    data_format: DataFormat
    specification_version: Optional[str]
    implementation_versions: Optional[List[str]]
    message_size: int
    checksum: str
    record_uri: Optional[str]

    class Config:
        extra = "forbid"
        frozen = True
