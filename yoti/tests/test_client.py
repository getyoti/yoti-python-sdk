# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti.client import Client


def test_client():
    app_id = 'app_id'
    app_key = 'app_key'
    client = Client(app_id, app_key)

    assert client.app_id == app_id
    assert client.app_key == app_key
