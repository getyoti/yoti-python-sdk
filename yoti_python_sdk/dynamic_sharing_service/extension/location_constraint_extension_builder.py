# -*- coding: utf-8 -*-
from __future__ import unicode_literals


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
        if not isinstance(latitude, float) and not isinstance(latitude, int):
            raise ValueError("Latitude must be float or int")
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        self.__device_location["latitude"] = latitude
        return self

    def with_longitude(self, longitude):
        if not isinstance(longitude, float) and not isinstance(longitude, int):
            raise ValueError("Lontitude must be float or int")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        self.__device_location["longitude"] = longitude
        return self

    def with_radius(self, radius):
        if not isinstance(radius, float) and not isinstance(radius, int):
            raise ValueError("Radius must be float or int")
        if not 0 <= radius:
            raise ValueError("Radius must be >= 0")
        self.__device_location["radius"] = radius
        return self

    def with_uncertainty(self, uncertainty):
        if not isinstance(uncertainty, float) and not isinstance(uncertainty, int):
            raise ValueError("Uncertainty must be float or int")
        if not 0 <= uncertainty:
            raise ValueError("Uncertainty must be >= 0")
        self.__device_location["max_uncertainty_radius"] = uncertainty
        return self

    def build(self):
        return self.__extension.copy()
