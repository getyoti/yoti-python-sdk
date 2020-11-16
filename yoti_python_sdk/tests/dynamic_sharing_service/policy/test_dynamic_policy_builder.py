from yoti_python_sdk.dynamic_sharing_service.policy.dynamic_policy_builder import (
    DynamicPolicyBuilder,
)
from yoti_python_sdk.dynamic_sharing_service.policy.wanted_attribute_builder import (
    WantedAttributeBuilder,
)
from yoti_python_sdk.dynamic_sharing_service.policy.source_constraint_builder import (
    SourceConstraintBuilder,
)

from yoti_python_sdk import config


def test_an_attribute_can_only_exist_once():
    NAME = "Test name"

    wanted_attribute = WantedAttributeBuilder().with_name(NAME).build()

    policy = (
        DynamicPolicyBuilder()
        .with_wanted_attribute(wanted_attribute)
        .with_wanted_attribute(wanted_attribute)
        .build()
    )

    assert len(policy["wanted"]) == 1
    assert wanted_attribute in policy["wanted"]


def test_remember_me():
    policy = DynamicPolicyBuilder().with_wanted_remember_me().build()

    assert policy["wanted_remember_me"]


def test_build_with_simple_attributes():
    builder = DynamicPolicyBuilder()
    builder.with_family_name()
    builder.with_given_names()
    builder.with_full_name()
    builder.with_date_of_birth()
    builder.with_gender()
    builder.with_postal_address()
    builder.with_structured_postal_address()
    builder.with_nationality()
    builder.with_phone_number()
    builder.with_selfie()
    builder.with_email()
    builder.with_document_details()
    builder.with_document_images()
    policy = builder.build()

    attr_names = [attr["name"] for attr in policy["wanted"]]
    assert len(policy["wanted"]) == 13
    assert config.ATTRIBUTE_FAMILY_NAME in attr_names
    assert config.ATTRIBUTE_GIVEN_NAMES in attr_names
    assert config.ATTRIBUTE_FULL_NAME in attr_names
    assert config.ATTRIBUTE_DATE_OF_BIRTH in attr_names
    assert config.ATTRIBUTE_GENDER in attr_names
    assert config.ATTRIBUTE_POSTAL_ADDRESS in attr_names
    assert config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS in attr_names
    assert config.ATTRIBUTE_NATIONALITY in attr_names
    assert config.ATTRIBUTE_PHONE_NUMBER in attr_names
    assert config.ATTRIBUTE_SELFIE in attr_names
    assert config.ATTRIBUTE_EMAIL_ADDRESS in attr_names
    assert config.ATTRIBUTE_DOCUMENT_DETAILS in attr_names
    assert config.ATTRIBUTE_DOCUMENT_IMAGES in attr_names


def test_build_with_age_derived_attributes():
    builder = DynamicPolicyBuilder()
    builder.with_age_over(18)
    builder.with_age_under(30)
    builder.with_age_under(40)
    policy = builder.build()

    attrs = [attr["derivation"] for attr in policy["wanted"]]
    assert len(attrs) == 3
    assert config.ATTRIBUTE_AGE_OVER + "18" in attrs
    assert config.ATTRIBUTE_AGE_UNDER + "30" in attrs
    assert config.ATTRIBUTE_AGE_UNDER + "40" in attrs


def test_a_derivation_can_exist_only_once():
    policy = DynamicPolicyBuilder().with_age_under(30).with_age_under(30).build()

    assert len(policy["wanted"]) == 1
    assert config.ATTRIBUTE_AGE_UNDER + "30" in [
        a["derivation"] for a in policy["wanted"]
    ]


def test_wanted_auth_types():
    policy = (
        DynamicPolicyBuilder()
        .with_selfie_auth()
        .with_pin_auth()
        .with_wanted_auth_type(99)
        .build()
    )

    assert len(policy["wanted_auth_types"]) == 3
    assert DynamicPolicyBuilder.SELFIE_AUTH_TYPE in policy["wanted_auth_types"]
    assert DynamicPolicyBuilder.PIN_AUTH_TYPE in policy["wanted_auth_types"]
    assert 99 in policy["wanted_auth_types"]


def test_build_with_auth_types_false():
    policy = DynamicPolicyBuilder().with_selfie_auth(False).build()

    assert len(policy["wanted_auth_types"]) == 0


def test_auth_types_can_exist_only_once():
    policy = (
        DynamicPolicyBuilder()
        .with_selfie_auth(True)
        .with_selfie_auth(False)
        .with_pin_auth()
        .with_pin_auth()
        .build()
    )

    assert len(policy["wanted_auth_types"]) == 1
    assert DynamicPolicyBuilder.SELFIE_AUTH_TYPE not in policy["wanted_auth_types"]
    assert DynamicPolicyBuilder.PIN_AUTH_TYPE in policy["wanted_auth_types"]


def test_attributes_with_constraints():
    constraint = SourceConstraintBuilder().with_national_id().build()
    policy = DynamicPolicyBuilder().with_nationality(constraints=constraint).build()
    assert len(policy["wanted"][0]["constraints"]) == 1


def test_attributes_with_accept_self_asserted_true():
    policy = DynamicPolicyBuilder().with_nationality(accept_self_asserted=True).build()
    assert policy["wanted"][0]["accept_self_asserted"] is True


def test_attributes_with_accept_self_asserted_false():
    policy = DynamicPolicyBuilder().with_nationality(accept_self_asserted=False).build()
    assert policy["wanted"][0]["accept_self_asserted"] is False


def test_attributes_without_accept_self_asserted():
    policy = DynamicPolicyBuilder().with_nationality().build()
    assert not hasattr(policy["wanted"][0], "accept_self_asserted")
