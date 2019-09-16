from yoti_python_sdk.exceptions import MalformedAgeVerificationException
from yoti_python_sdk import config


class AgeVerification(object):
    def __init__(self, derived_attribute):
        self.__derived_attribute = derived_attribute

        split = derived_attribute.name.split(":")
        if len(split) != 2:
            raise MalformedAgeVerificationException

        if (
            split[0] in config.ATTRIBUTE_AGE_OVER
            or split[0] in config.ATTRIBUTE_AGE_UNDER
        ):
            self.__check_type = split[0]
        else:
            raise MalformedAgeVerificationException

        try:
            self.__age_verified = int(split[1])
            if derived_attribute.value == "true":
                self.__result = True
            elif derived_attribute.value == "false":
                self.__result = False
        except Exception:
            raise MalformedAgeVerificationException

    @property
    def age(self):
        return self.__age_verified

    @property
    def check_type(self):
        return self.__check_type

    @property
    def result(self):
        return self.__result

    @property
    def attribute(self):
        return self.__derived_attribute
