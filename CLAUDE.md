# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A retrieve plugin for **dserver** (the dtool lookup server, package `dservercore`). It implements
MongoDB-backed dataset registration and retrieval of the per-dataset documents (README, manifest,
annotations, tags). The plugin is discovered by dserver at runtime through the `dservercore.retrieve`
entry point declared in `pyproject.toml`:

```
[project.entry-points."dservercore.retrieve"]
MongoRetrieve = "dserver_retrieve_plugin_mongo.utils_retrieve:MongoRetrieve"
```

This package is a *companion* to `dserver-search-plugin-mongo`: retrieve and search are separate
plugins that, in the common deployment, point at the *same* MongoDB collection (the test fixtures
wire `RETRIEVE_MONGO_*` and `SEARCH_MONGO_*` to one temp database). The search plugin answers queries
and returns trimmed dataset records; this plugin fetches the heavy per-dataset content by URI.

## Architecture

The entire plugin is one class, `MongoRetrieve(RetrieveABC)` in
`dserver_retrieve_plugin_mongo/utils_retrieve.py`, implementing the abstract interface from
`dservercore.RetrieveABC`:

- `init_app(app)` — pulls `RETRIEVE_MONGO_URI`/`_DB`/`_COLLECTION` from Flask `app.config` and opens
  the `MongoClient`. Unlike the search plugin, it does *not* create any index.
- `register_dataset(dataset_info)` — upserts a dataset record keyed on `(uuid, uri)`. Converts
  `frozen_at`/`created_at` to datetimes via `dservercore.date_utils`. Wraps
  `pymongo.errors.DocumentTooLarge` into `dservercore.ValidationError`. Also stores a parsed copy of
  the README under `readme_parsed` (see below).
- Getters `get_readme(uri)` / `get_manifest(uri)` / `get_annotations(uri)` / `get_tags(uri)` — fetch
  the record by `uri` and return the corresponding field; raise `dservercore.UnknownURIError` when no
  record matches.
- Mutators `set_annotations(uri, …)` / `set_tags(uri, …)` / `set_readme(uri, …)` — `$set` the
  respective field on the matching record, raising `UnknownURIError` when no record matches.
  `set_readme` also re-parses and updates `readme_parsed`.
- `get_config` / `get_config_secrets_to_obfuscate` — expose `config.Config` and the secret list to
  dserver's `/config` route.

Note `register_dataset` and the `(uuid, uri)` upsert logic are duplicated near-verbatim from the
search plugin — the two plugins register the same documents into the shared collection.

### README parsing (`readme_parsed`)

The README is stored verbatim as a string under `readme`. `_parse_readme(readme)` additionally
YAML-parses it (returning the dict, or `None` on failure / non-dict) and the result is stored under
`readme_parsed`. This enables structured queries over README content by *co-installed* plugins —
e.g. the dependency-graph plugin's `readme_parsed.derived_from.uuid` dependency key. `readme_parsed`
is written by `register_dataset` and refreshed by `set_readme`. Requires `PyYAML`.

### Configuration

`config.py` defines `Config` (env-var-backed defaults) and `CONFIG_SECRETS_TO_OBFUSCATE`. Note the
default `RETRIEVE_MONGO_DB` in `Config` is `"dtool_info"`, while the README example uses `"dserver"`.

## Commands

```bash
# Install for development (with test deps)
pip install .[test]

# The test extras also need the server core + search plugin:
pip install dservercore dserver-search-plugin-mongo

# Run the full test suite (pytest config + coverage live in pyproject.toml)
pytest

# Run a single test file / single test
pytest tests/test_utils_retrieve_standalone.py
pytest tests/test_utils_retrieve_standalone.py::test_functional

# Lint (matches CI)
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 .   # full run
```

### A running MongoDB is required for most tests

Tests connect to `mongodb://localhost:27017` by default, overridable via the `TEST_MONGO_URI` env var
(used in `tests/test_utils_retrieve_standalone.py`, `tests/conftest.py` and
`tests/test_config_route.py`, e.g. for an authenticated MongoDB). They create a randomly-named temp
database per test and drop it (and close the client) on teardown.

The test app config also sets bare `MONGO_URI`/`MONGO_DB`/`MONGO_COLLECTION` keys (in addition to the
`RETRIEVE_MONGO_*` / `SEARCH_MONGO_*` ones) so co-installed plugins like the dependency-graph plugin
can initialise against the same temp database.

## Testing structure

- `tests/test_utils_retrieve_standalone.py` — exercises `MongoRetrieve` directly via a `_MockApp`
  holding a `config` dict (no Flask). Builds real dtool datasets with `DataSetCreator`, registers
  them, and asserts the getters/mutators. This is the file to extend when changing retrieval logic.
- `tests/test_config_route.py` and `tests/conftest.py` — full Flask-app integration via
  `dservercore.create_app`. `tmp_app_with_users` builds an in-memory SQLite app with JWT users and
  permissions, wiring both retrieve and search plugins to the same temp Mongo db. Use this for
  route-level behavior (e.g. `/config/info`, `/config/versions`).
- `tests/utils.py` — `compare_nested` does partial/marked dict comparison; `make_marker` builds the
  comparison mask.

## Versioning & packaging

The build backend is **flit** (`flit_scm:buildapi`, configured in `pyproject.toml`); there is no
`setup.cfg`/`setup.py`. pytest and coverage config also live in `pyproject.toml` under
`[tool.pytest.ini_options]`.

Version is managed by `setuptools_scm` (via `flit_scm`) from git tags (`guess-next-dev`,
`no-local-version`), written to `dserver_retrieve_plugin_mongo/version.py` (generated, not committed).
`__init__.py` resolves the version at runtime first via `importlib.metadata`, falling back to the
generated `version.py`.

Releases are tag-driven: pushing a tag triggers `.github/workflows/publish.yml` (trusted publishing
to PyPI + GitHub release + Zenodo). Update `CHANGELOG.rst` (keep-a-changelog format, semver) when
preparing a release.

## CI

`.github/workflows/test.yml` runs a matrix of Python 3.10–3.13 × MongoDB 5.0/6.0/7.0/8.0, installing
`dservercore` and `dserver-search-plugin-mongo` from their `main` branches. Keep the plugin
compatible with that whole range; `pyproject.toml` declares `requires-python = ">=3.10"` to match.
