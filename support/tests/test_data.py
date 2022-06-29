from linuxforhealth.healthos.support.data import MetaRecord
from pytest import fixture
from typing import Dict


@fixture
def meta_data() -> Dict:
    """Returns a metadata fixture"""
    return {
        "uuid": "068e56aa-4c07-492f-a801-64242ddaf2f4",
        "creation_date": "2022-06-29T19:25:16.248395",
        "data_format": "FHIR_JSON",
        "specification_version": "4.0.1",
        "implementation_versions": [
            "https://bluebutton.cms.gov/assets/ig/StructureDefinition-bluebutton-patient-claim.html"
        ],
        "message_size": 509,
        "checksum": "d7a928f396efa0bb15277991bd8d4d9a2506d751f9de8b344c1a3e5f8c45a409",
        "record_uri": "https://super-server/fhir-server/api/v4/Patient/12345"
    }


def test_meta_record_all_fields(meta_data):
    MetaRecord(**meta_data)


def test_meta_record_defaulted_fields(meta_data):
    del meta_data["uuid"]
    del meta_data["creation_date"]
    meta_record = MetaRecord(**meta_data)

    assert meta_record.uuid is not None
    assert meta_record.creation_date is not None


def test_meta_record_remove_optional_fields(meta_data):
    del meta_data["specification_version"]
    del meta_data["implementation_versions"]
    del meta_data["record_uri"]

    meta_record = MetaRecord(**meta_data)

    assert meta_record.specification_version is None
    assert meta_record.implementation_versions is None
    assert meta_record.record_uri is None
