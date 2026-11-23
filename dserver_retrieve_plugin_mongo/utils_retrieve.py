"""Mongo retrieve plugin module."""

import yaml

import pymongo.errors

from pymongo import MongoClient

from dservercore import RetrieveABC, ValidationError, UnknownURIError

from dservercore.date_utils import (
    extract_created_at_as_datetime,
    extract_frozen_at_as_datetime,
)

from dserver_retrieve_plugin_mongo.config import (
    Config, CONFIG_SECRETS_TO_OBFUSCATE)


def _parse_readme(readme):
    """Return the README parsed into a dict, or None.

    The README is stored verbatim as a string under 'readme'. The parsed
    representation stored under 'readme_parsed' enables structured queries
    over README content, e.g. the dependency graph plugin's
    'readme_parsed.derived_from.uuid' dependency key.
    """
    if isinstance(readme, dict):
        return readme
    if isinstance(readme, str):
        try:
            parsed = yaml.safe_load(readme)
        except yaml.YAMLError:
            return None
        if isinstance(parsed, dict):
            return parsed
    return None


def _register_dataset_descriptive_metadata(collection, dataset_info):
    """Register dataset info in the collection.

    If the "uuid" and "uri" are the same as another record in
    the mongodb collection a new record is not created, and
    the UUID is returned.

    Returns UUID of dataset otherwise.
    """

    # Make a copy to ensure that the original data strucutre does not
    # get mangled by the datetime replacements.
    dataset_info = dataset_info.copy()

    # Store a parsed representation of the README alongside the verbatim
    # string to enable structured queries over README content.
    dataset_info["readme_parsed"] = _parse_readme(dataset_info.get("readme"))

    frozen_at = extract_frozen_at_as_datetime(dataset_info)
    created_at = extract_created_at_as_datetime(dataset_info)

    dataset_info["frozen_at"] = frozen_at
    dataset_info["created_at"] = created_at

    query = {"uuid": dataset_info["uuid"], "uri": dataset_info["uri"]}

    # If a record with the same UUID and URI exists return the uuid
    # without adding a duplicate record.
    exists = collection.find_one(query)

    if exists is None:
        collection.insert_one(dataset_info)
    else:
        collection.find_one_and_replace(query, dataset_info)

    # The MongoDB client dynamically updates the dataset_info dict
    # with and '_id' key. Remove it.
    if "_id" in dataset_info:
        del dataset_info["_id"]

    return dataset_info["uuid"]


class MongoRetrieve(RetrieveABC):
    """Mongo implementation of the retrieve module."""

    def init_app(self, app):
        try:
            self._mongo_uri = app.config["RETRIEVE_MONGO_URI"]
            self.client = MongoClient(self._mongo_uri,
                                      uuidRepresentation='standard')
        except KeyError:
            raise(RuntimeError("Please set the RETRIEVE_MONGO_URI environment variable"))  # NOQA

        try:
            self._mongo_db = app.config["RETRIEVE_MONGO_DB"]
            self.db = self.client[self._mongo_db]
        except KeyError:
            raise(RuntimeError("Please set the RETRIEVE_MONGO_DB environment variable"))  # NOQA

        try:
            self._mongo_collection = app.config["RETRIEVE_MONGO_COLLECTION"]
            self.collection = self.db[self._mongo_collection]
        except KeyError:
            raise(RuntimeError("Please set the RETRIEVE_MONGO_COLLECTION environment variable"))  # NOQA

    def register_dataset(self, dataset_info):
        try:
            return _register_dataset_descriptive_metadata(self.collection, dataset_info)
        except pymongo.errors.DocumentTooLarge as e:
            raise (ValidationError("Dataset has too much metadata: {}".format(e)))

    def get_readme(self, uri) -> str:
        item = self.collection.find_one({"uri": uri})
        if item is None:
            raise (UnknownURIError())
        return item["readme"]

    def get_manifest(self, uri):
        """Return a dataset's maifest."""
        item = self.collection.find_one({"uri": uri})
        if item is None:
            raise (UnknownURIError())
        return item["manifest"]

    def get_annotations(self, uri):
        """Return a dataset's annotations."""
        item = self.collection.find_one({"uri": uri})
        if item is None:
            raise (UnknownURIError())
        return item["annotations"]

    def set_annotations(self, uri, annotations):
        """Set a dataset's annotations (replaces existing annotations)."""
        result = self.collection.update_one(
            {"uri": uri},
            {"$set": {"annotations": annotations}}
        )
        if result.matched_count == 0:
            raise (UnknownURIError())
        return annotations

    def get_tags(self, uri):
        """Return a dataset's tags."""
        item = self.collection.find_one({"uri": uri})
        if item is None:
            raise (UnknownURIError())
        return item["tags"]

    def set_tags(self, uri, tags):
        """Set a dataset's tags (replaces existing tags)."""
        result = self.collection.update_one(
            {"uri": uri},
            {"$set": {"tags": tags}}
        )
        if result.matched_count == 0:
            raise (UnknownURIError())
        return tags

    def set_readme(self, uri, readme):
        """Set a dataset's readme content."""
        result = self.collection.update_one(
            {"uri": uri},
            {"$set": {"readme": readme,
                      "readme_parsed": _parse_readme(readme)}}
        )
        if result.matched_count == 0:
            raise (UnknownURIError())
        return readme

    def get_config(self):
        """Return initial Config object, available app-instance independent."""
        return Config

    def get_config_secrets_to_obfuscate(self):
        """Return config secrets never to be exposed clear text."""
        return CONFIG_SECRETS_TO_OBFUSCATE
