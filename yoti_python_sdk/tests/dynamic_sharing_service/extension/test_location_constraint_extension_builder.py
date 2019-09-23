# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.dynamic_sharing_service.extension.location_constraint_extension_builder import (
    LocationConstraintExtensionBuilder,
)
import pytest


def test_longitude_validation():
    extension = LocationConstraintExtensionBuilder()
    with pytest.raises(ValueError):
        extension.with_longitude(270.00)
    with pytest.raises(ValueError):
        extension.with_longitude(-181)
    with pytest.raises(ValueError):
        extension.with_longitude("27.00")
    extension.with_longitude(180.0)
    extension.with_longitude(-90)


def test_latitude_validation():
    extension = LocationConstraintExtensionBuilder()
    with pytest.raises(ValueError):
        extension.with_latitude(270.00)
    with pytest.raises(ValueError):
        extension.with_latitude(-181)
    with pytest.raises(ValueError):
        extension.with_latitude("27.00")
    with pytest.raises(ValueError):
        extension.with_latitude(91)
    with pytest.raises(ValueError):
        extension.with_latitude(-180)
    extension.with_latitude(18.0)
    extension.with_latitude(-90)


def test_uncertainty_validation():
    extension = LocationConstraintExtensionBuilder()
    with pytest.raises(ValueError):
        extension.with_uncertainty(-1)
    with pytest.raises(ValueError):
        extension.with_uncertainty(-0.01)
    with pytest.raises(ValueError):
        extension.with_uncertainty("3")
    extension.with_uncertainty(0)
    extension.with_uncertainty(1)
    extension.with_uncertainty(1e3)


def test_radius_validation():
    extension = LocationConstraintExtensionBuilder()
    with pytest.raises(ValueError):
        extension.with_radius(-1)
    with pytest.raises(ValueError):
        extension.with_radius(-0.01)
    with pytest.raises(ValueError):
        extension.with_radius("3")
    extension.with_radius(0)
    extension.with_radius(1)
    extension.with_radius(1e3)


def test_builds_with_given_values():
    LATITUDE = 50
    LONGITUDE = 99
    RADIUS = 60
    UNCERTAINTY = 30

    extension = (
        LocationConstraintExtensionBuilder()
        .with_latitude(LATITUDE)
        .with_longitude(LONGITUDE)
        .with_radius(RADIUS)
        .with_uncertainty(UNCERTAINTY)
        .build()
    )

    device_location = extension["content"]["expected_device_location"]

    assert device_location["latitude"] == LATITUDE
    assert device_location["longitude"] == LONGITUDE
    assert device_location["radius"] == RADIUS
    assert device_location["max_uncertainty_radius"] == UNCERTAINTY
