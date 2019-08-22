from yoti_python_sdk.sandbox.attribute import SandboxAttribute
from yoti_python_sdk import config


class SandboxAgeVerification(object):
    def __init__(self, date_of_birth, supported_age_derivation, anchors=None):

        if anchors is None:
            anchors = []

        self.__date_of_birth = date_of_birth
        self.__supported_age_derivation = supported_age_derivation
        self.__anchors = anchors

    def to_attribute(self):
        return (
            SandboxAttribute.builder()
            .with_name(config.ATTRIBUTE_DATE_OF_BIRTH)
            .with_value(self.__date_of_birth)
            .with_derivation(self.__supported_age_derivation)
            .with_anchors(self.__anchors)
            .build()
        )

    @staticmethod
    def builder():
        return SandboxAgeVerificationBuilder()


class SandboxAgeVerificationBuilder(object):
    def __init__(self):
        self.__date_of_birth = None
        self.__derivation = None
        self.__anchors = None

    def with_date_of_birth(self, date_of_birth):
        self.__date_of_birth = date_of_birth
        return self

    def with_derivation(self, derivation):
        self.__derivation = derivation
        return self

    def with_age_over(self, age_over):
        return self.with_derivation(config.ATTRIBUTE_AGE_OVER + str(age_over))

    def with_age_under(self, age_under):
        return self.with_derivation(config.ATTRIBUTE_AGE_UNDER + str(age_under))

    def with_anchors(self, anchors):
        self.__anchors = anchors
        return self

    def build(self):
        return SandboxAgeVerification(
            self.__date_of_birth, self.__derivation, self.__anchors
        )
