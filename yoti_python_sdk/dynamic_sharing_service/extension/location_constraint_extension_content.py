# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ExpectedDeviceLocation(object):
    def __init__(self, latitude, longtitude, radius=None, uncertainty=None):
        self.__latitude = latitude
        self.__longtitude = longtitude
        self.__radius = radius
        self.__uncertainty = uncertainty

    @property
    def latitude(self):
        return self.__latitude

    @property
    def longtitude(self):
        return self.__longtitude

    @property
    def radius(self):
        return self.__radius

    @property
    def uncertainty(self):
        return self.__uncertainty

    @property
    def data(self):
        return {
            "latitude": self.__latitude,
            "longtitude": self.__longtitude,
            "radius": self.__radius,
            "uncertainty": self.__uncertainty,
        }
