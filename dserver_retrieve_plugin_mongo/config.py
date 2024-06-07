import os

CONFIG_SECRETS_TO_OBFUSCATE = [
    "RETRIEVE_MONGO_URI",
    "RETRIEVE_MONGO_DB",
    "RETRIEVE_MONGO_COLLECTION",
]


class Config(object):
    RETRIEVE_MONGO_URI = os.environ.get("RETRIEVE_MONGO_URI", "mongodb://localhost:27017/")
    RETRIEVE_MONGO_DB = os.environ.get("RETRIEVE_MONGO_DB", "dtool_info")
    RETRIEVE_MONGO_COLLECTION = os.environ.get("RETRIEVE_MONGO_COLLECTION", "datasets")