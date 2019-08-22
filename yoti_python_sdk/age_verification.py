class AgeVerification(object):
    def __init__(self, derived_attribute):
        self.__derived_attribute = derived_attribute

        split = derived_attribute.name.split(":")
        self.__check_type = split[0]
        self.__age_verified = int(split[1])

        if derived_attribute.value == "true":
            self.__result = True
        elif derived_attribute.value == "false":
            self.__result = False

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
