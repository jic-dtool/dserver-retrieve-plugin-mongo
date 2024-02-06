"""Test the dserver-retrieve-plugin-mongo package."""


def test_version_is_string():
    import dserver_retrieve_plugin_mongo
    assert isinstance(dserver_retrieve_plugin_mongo.__version__, str)
