"""Test the /config blueprint route."""

import json
import dserver_retrieve_plugin_mongo

from .utils import compare_nested


def test_config_info_route(tmp_app_with_users, snowwhite_token):  # NOQA

    headers = dict(Authorization="Bearer " + snowwhite_token)
    r = tmp_app_with_users.get(
        "/config/info",
        headers=headers,
    )
    assert r.status_code == 200

    expected_content = {
          'retrieve_mongo_collection': 'datasets',
          'retrieve_mongo_uri': 'mongodb://localhost:27017/',
    }

    response = json.loads(r.data.decode("utf-8"))

    assert "config" in response
    assert compare_nested(expected_content, response["config"])


def test_config_version_route(tmp_app_with_users):  # NOQA

    r = tmp_app_with_users.get(
        "/config/versions",
    )
    assert r.status_code == 200

    expected_content = {
          'dserver_retrieve_plugin_mongo': dserver_retrieve_plugin_mongo.__version__,
    }

    response = json.loads(r.data.decode("utf-8"))

    assert "versions" in response
    assert compare_nested(expected_content, response["versions"])
