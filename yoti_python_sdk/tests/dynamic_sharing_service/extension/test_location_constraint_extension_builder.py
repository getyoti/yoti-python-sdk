# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.dynamic_sharing_service.extension.location_constraint_extension_builder import (
    LocationConstraintExtensionBuilder,
)


def test_builds_with_given_values():
    LATITUDE = 50
    LONGTITUDE = 99
    RADIUS = 60
    UNCERTAINTY = 30

    extension = (
        LocationConstraintExtensionBuilder()
        .with_latitude(LATITUDE)
        .with_longtitude(LONGTITUDE)
        .with_radius(RADIUS)
        .with_uncertainty(UNCERTAINTY)
        .build()
    )

    device_location = extension["content"]["expected_device_location"]

    assert device_location["latitude"] == LATITUDE
    assert device_location["longtitude"] == LONGTITUDE
    assert device_location["radius"] == RADIUS
    assert device_location["max_uncertainty_radius"] == UNCERTAINTY
