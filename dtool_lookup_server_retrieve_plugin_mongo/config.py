import json
import os

import dtool_lookup_server_retrieve_plugin_mongo


class Config(object):
    RETRIEVE_MONGO_URI = os.environ.get("RETRIEVE_MONGO_URI", "mongodb://localhost:27017/")
    RETRIEVE_MONGO_DB = os.environ.get("RETRIEVE_MONGO_DB", "dtool_info")
    RETRIEVE_MONGO_COLLECTION = os.environ.get("RETRIEVE_MONGO_COLLECTION", "datasets")

    @classmethod
    def to_dict(cls):
        """Convert server configuration into dict."""
        exclusions = [
            # sensitive data, i.e. password
        ]  # config keys to exclude
        d = {"version": dtool_lookup_server_retrieve_plugin_mongo.__version__}
        for k, v in cls.__dict__.items():
            # select only capitalized fields
            if k.upper() == k and k not in exclusions:
                d[k.lower()] = v
        return d
