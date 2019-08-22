from yoti_python_sdk.attribute import Attribute


class AgeVerification(object):
    def __init__(self, derived_attribute: Attribute):
        self.__derived_attribute = derived_attribute

        split = derived_attribute.name.split(":")
        self.__check_type = split[0]
        self.__age_verified = int(split[1])
        self.__result = bool(derived_attribute.value)

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
