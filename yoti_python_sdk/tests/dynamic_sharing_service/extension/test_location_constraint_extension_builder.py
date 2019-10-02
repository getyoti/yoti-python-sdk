# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.dynamic_sharing_service.extension.location_constraint_extension_builder import (
    LocationConstraintExtensionBuilder,
)
import pytest


@pytest.mark.parametrize("longitude", [270.00, -181, "27.00"])
def test_longitude_validation_should_reject_invalid(longitude):
    extension = LocationConstraintExtensionBuilder()
    with pytest.raises(ValueError):
        extension.with_longitude(longitude)


@pytest.mark.parametrize("longitude", [180.0, -90])
def test_longitude_vaidation_should_accept_valid(longitude):
    extension = LocationConstraintExtensionBuilder()
    extension.with_longitude(longitude)


@pytest.mark.parametrize("latitude", [270.00, -181, "27.00", 91, -180])
def test_latitude_validation_should_reject_invalid(latitude):
    extension = LocationConstraintExtensionBuilder()
    with pytest.raises(ValueError):
        extension.with_latitude(latitude)


@pytest.mark.parametrize("latitude", [18.0, -90])
def test_latitude_validation_should_accept_valid(latitude):
    extension = LocationConstraintExtensionBuilder()
    extension.with_latitude(latitude)


@pytest.mark.parametrize("uncertainty", [-1, -0.01, "3"])
def test_uncertainty_validation_should_reject_invalid(uncertainty):
    extension = LocationConstraintExtensionBuilder()
    with pytest.raises(ValueError):
        extension.with_uncertainty(uncertainty)


@pytest.mark.parametrize("uncertainty", [0, 1, 1e3])
def test_uncertainty_validation_should_accept_valid(uncertainty):
    extension = LocationConstraintExtensionBuilder()
    extension.with_uncertainty(uncertainty)


@pytest.mark.parametrize("radius", [-1, -0.01, "3"])
def test_radius_validation_should_reject_invalid(radius):
    extension = LocationConstraintExtensionBuilder()
    with pytest.raises(ValueError):
        extension.with_radius(radius)


@pytest.mark.parametrize("radius", [0, 1, 1e3])
def test_radius_validation_should_accept_valid(radius):
    extension = LocationConstraintExtensionBuilder()
    extension.with_radius(radius)


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
