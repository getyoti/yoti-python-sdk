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
        """
        Converts the age verification object into an Attribute

        :return: Instance of SandboxAttribute
        """
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
        """
        Creates a sandbox age verification builder

        :return: Instance of SandboxAgeVerificationBuilder
        """
        return SandboxAgeVerificationBuilder()


class SandboxAgeVerificationBuilder(object):
    def __init__(self):
        self.__date_of_birth = None
        self.__derivation = None
        self.__anchors = None

    def with_date_of_birth(self, date_of_birth):
        """
        Set the date of birth on the builder

        :param str date_of_birth: the date of birth
        :return: the updated builder
        """
        self.__date_of_birth = date_of_birth
        return self

    def with_derivation(self, derivation):
        """
        Set the derivation of the age verification

        :param str derivation: the derivation
        :return: the updated builder
        """
        self.__derivation = derivation
        return self

    def with_age_over(self, age_over):
        """
        Set the age over value of the age verification

        :param int age_over: the age over value
        :return: the updated builder
        """
        return self.with_derivation(config.ATTRIBUTE_AGE_OVER + str(age_over))

    def with_age_under(self, age_under):
        """
        Set the age under value of the age verification

        :param int age_under:
        :return: the updated builder
        """
        return self.with_derivation(config.ATTRIBUTE_AGE_UNDER + str(age_under))

    def with_anchors(self, anchors):
        """
        Set the anchors for the age verification

        :param list[SandboxAnchor] anchors:
        :return: the updated builder
        """
        self.__anchors = anchors
        return self

    def build(self):
        return SandboxAgeVerification(
            self.__date_of_birth, self.__derivation, self.__anchors
        )
