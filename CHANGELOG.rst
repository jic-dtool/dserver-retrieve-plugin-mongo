CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.

[Unreleased]
------------

Changed
^^^^^^^

- Dropped support for Python 3.7–3.9; minimum is now Python 3.10
- Updated CI Python matrix to 3.10–3.13; updated MongoDB matrix to 5.0–8.0

Fixed
^^^^^

- Test fixtures: hardcoded MongoDB URI replaced by ``TEST_MONGO_URI`` environment variable (default: ``mongodb://localhost:27017/``)
- Test fixtures: added ``client.close()`` after ``drop_database()`` in teardown to prevent connection pool exhaustion
- Test fixtures: removed stale ``FLASK_ENV`` key from app config (removed in Flask 3.0)
- Config route test: URI assertion now reads from ``TEST_MONGO_URI`` environment variable

[0.4.2]
-------

Added
^^^^^

- Automated github release
- Zenodo integration
- Trusted publishing on PyPI


[0.4.1]
-------

Changed
^^^^^^^

- Changed URLs from ``livMatS`` prefix to ``jic-dtool`` prefix.


[0.4.0]
-------

Changed
^^^^^^^

- Changed dependency from ``dtool_lookup_server`` to ``dservercore``.

[0.3.0]
-------

Added
^^^^^

- Tag retrieval function

Changed
^^^^^^^

- Replace ``setup.py`` by ``pyproject.toml``
- Rebranded from ``dtool-lookup-server-retrieve-plugin-mongo`` to shorter ``dserver-retrieve-plugin-mongo``

Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^


Security
^^^^^^^^


