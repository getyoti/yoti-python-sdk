from yoti_python_sdk.attribute import Attribute
from yoti_python_sdk.age_verification import AgeVerification
from yoti_python_sdk.exceptions import MalformedAgeVerificationException
from yoti_python_sdk import config
import pytest


@pytest.fixture(scope="module")
def age_over_attribute():
    return Attribute(config.ATTRIBUTE_AGE_OVER + "18", "true", None)


@pytest.fixture(scope="module")
def age_under_attribute():
    return Attribute(config.ATTRIBUTE_AGE_UNDER + "18", "false", None)


@pytest.mark.parametrize(
    "age_verification_name",
    [":age_over:18", "age_over:18:", "ageover:18", "age_over:", "age_over::18"],
)
def test_malformed_age_verification_attributes(age_verification_name):
    with pytest.raises(MalformedAgeVerificationException):
        attribute = Attribute(age_verification_name, "true", None)
        age_verification_name = AgeVerification(attribute)


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
