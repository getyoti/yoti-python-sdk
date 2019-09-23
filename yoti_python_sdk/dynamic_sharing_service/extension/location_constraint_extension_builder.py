# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from deprecated import deprecated


class LocationConstraintExtensionBuilder(object):
    LOCATION_CONSTRAINT = "LOCATION_CONSTRAINT"

    def __init__(self):
        self.__extension = {}
        self.__extension["type"] = self.LOCATION_CONSTRAINT
        self.__extension["content"] = {}
        self.__device_location = {
            "latitude": None,
            "longitude": None,
            "radius": None,
            "max_uncertainty_radius": None,
        }
        self.__extension["content"]["expected_device_location"] = self.__device_location

    def with_latitude(self, latitude):
        self.__device_location["latitude"] = latitude
        return self

    @deprecated
    def with_longtitude(self, longtitude):
        """
        To be removed in v3.0.0
        Use with_longitude instead
        """
        return self.with_longitude(longtitude)

    def with_longitude(self, longitude):
        self.__device_location["longitude"] = longitude
        return self

    def with_radius(self, radius):
        self.__device_location["radius"] = radius
        return self

    def with_uncertainty(self, uncertainty):
        self.__device_location["max_uncertainty_radius"] = uncertainty
        return self

    def build(self):
        return self.__extension.copy()
