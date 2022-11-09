"""Test the dtool-lookup-server-retrieve-mongo-plugin package."""


def test_version_is_string():
    import dtool_lookup_server_retrieve_mongo_plugin
    assert isinstance(dtool_lookup_server_retrieve_mongo_plugin.__version__, str)
