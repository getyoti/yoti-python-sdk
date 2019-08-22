from yoti_python_sdk.attribute import Attribute
from yoti_python_sdk.age_verification import AgeVerification
from yoti_python_sdk import config
import pytest


@pytest.fixture(scope="module")
def age_over_attribute():
    return Attribute(config.ATTRIBUTE_AGE_OVER + "18", "true", None)


@pytest.fixture(scope="module")
def age_under_attribute():
    return Attribute(config.ATTRIBUTE_AGE_UNDER + "18", "false", None)


def test_create_age_verification_from_age_over_attribute(age_over_attribute):
    age_verification = AgeVerification(age_over_attribute)

    assert age_verification.age == 18
    assert age_verification.check_type in config.ATTRIBUTE_AGE_OVER
    assert age_verification.result is True


def test_create_age_verification_from_age_under_attribute(age_under_attribute):
    age_verification = AgeVerification(age_under_attribute)

    assert age_verification.age == 18
    assert age_verification.check_type in config.ATTRIBUTE_AGE_UNDER
    assert age_verification.result is False
