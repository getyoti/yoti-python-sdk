import json


class AmlResult:
    def __init__(self, response_text):
        try:
            self.on_pep_list = json.loads(response_text).get('on_pep_list')
            self.on_fraud_list = json.loads(response_text).get('on_fraud_list')
            self.on_watch_list = json.loads(response_text).get('on_watch_list')

        except Exception as exc:
            raise ValueError(
                'Could not retrieve AML values from response: {0}'.format(
                    exc))

        finally:
            self.__check_for_none_values(self.on_pep_list)
            self.__check_for_none_values(self.on_fraud_list)
            self.__check_for_none_values(self.on_watch_list)

    @staticmethod
    def __check_for_none_values(arg):
        if arg is None:
            raise TypeError(str.format("{0} argument was unable to be retrieved from the response", arg))

    def __iter__(self):
        yield 'on_pep_list', self.on_pep_list
        yield 'on_fraud_list', self.on_fraud_list
        yield 'on_watch_list', self.on_watch_list


class AmlAddress:
    def __init__(self, country, postcode=None):
        self.country = country
        self.post_code = postcode


class AmlProfile:
    def __init__(self, given_names, family_name, address, ssn=None):
        self.given_names = given_names
        self.family_name = family_name
        self.address = address.__dict__
        self.ssn = ssn
