# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .location_constraint_extension_content import ExpectedDeviceLocation
from .extension import Extension


class LocationConstraintExtensionBuilder(object):
    LOCATION_CONSTRAINT = "LOCATION_CONSTRAINT"

    def __init__(self):
        self.__extension = {}
        self.__extension["_Extension__extension_type"] = self.LOCATION_CONSTRAINT
        self.__latitude = None
        self.__longtitude = None
        self.__radius = None
        self.__uncertainty = None

    def with_latitude(self, latitude):
        self.__latitude = latitude
        return self

    def with_longtitude(self, longtitude):
        self.__longtitude = longtitude
        return self

    def with_radius(self, radius):
        self.__radius = radius
        return self

    def with_uncertainty(self, uncertainty):
        self.__uncertainty = uncertainty
        return self

    def build(self):
        self.__extension["_Extension__content"] = ExpectedDeviceLocation(
            self.__latitude, self.__longtitude, self.__radius, self.__uncertainty
        )
        return Extension(**self.__extension)
