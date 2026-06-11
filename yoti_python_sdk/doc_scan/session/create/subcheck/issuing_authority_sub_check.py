# -*- coding: utf-8 -*-

from yoti_python_sdk.doc_scan.session.create.filter.document_filter import DocumentFilter
from yoti_python_sdk.utils import YotiSerializable, remove_null_values


class IssuingAuthoritySubCheck(YotiSerializable):
    """
    Requests creation of an Issuing Authority Sub Check.
    """

    def __init__(self, filter=None):
        self._filter = filter

    @property
    def requested(self):
        return True

    @property
    def filter(self):
        return self._filter

    def to_json(self):
        return remove_null_values({"requested": self.requested, "filter": self.filter})


class IssuingAuthoritySubCheckBuilder:
    """
    Builder for Issuing Authority Sub Check.
    """
    def __init__(self):
        self._filter = None

    def with_filter(self, filter):
        if not issubclass(type(filter), DocumentFilter):
            raise ValueError('invalid filter')

        self._filter = filter

        return self

    def build(self):
        return IssuingAuthoritySubCheck(filter=self._filter)
