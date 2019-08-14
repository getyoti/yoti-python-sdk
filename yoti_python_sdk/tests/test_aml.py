import json

import pytest

from yoti_python_sdk import aml

VALID_RESPONSE = '{"on_fraud_list":false,"on_pep_list":false,"on_watch_list":true}'
INVALID_FORMAT_RESPONSE = json.loads(
    '{"on_fraud_list":false,"on_pep_list":false,"on_watch_list":true}'
)
MISSING_FRAUD_LIST_RESPONSE = '{"on_pep_list":false,"on_watch_list":true}'
VALID_AML_ADDRESS = aml.AmlAddress(country="FRA", postcode="ABC123")


def test_getting_aml_result_with_valid_response():
    aml.AmlResult(VALID_RESPONSE)


def test_getting_aml_result_with_invalid_format_response():
    with pytest.raises(RuntimeError) as exc:
        aml.AmlResult(INVALID_FORMAT_RESPONSE)
    expected_error = "Could not parse AML result from response"
    assert expected_error in str(exc.value)


def test_getting_aml_result_with_missing_value():
    with pytest.raises(TypeError):
        aml.AmlResult(MISSING_FRAUD_LIST_RESPONSE)


def test_getting_aml_result_with_empty_string_response():
    with pytest.raises(ValueError):
        aml.AmlResult("")


def test_getting_aml_result_with_none_value():
    with pytest.raises(ValueError):
        aml.AmlResult(None)


def test_setting_aml_address_with_valid_values():
    aml.AmlAddress(VALID_AML_ADDRESS)


def test_setting_aml_profile_with_valid_values():
    aml.AmlProfile(
        given_names="Joe", family_name="Bloggs", address=VALID_AML_ADDRESS, ssn="123456"
    )
