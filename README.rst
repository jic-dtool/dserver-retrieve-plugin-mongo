README
======

Retrieve plugin for dserver using mongodb

To install the dserver-retrieve-plugin-mongo package.

.. code-block:: bash

    cd dserver-retrieve-plugin-mongo
    python setup.py install


To configure the connection to the mongo database.

.. code-block:: bash

    export RETRIEVE_MONGO_URI="mongodb://localhost:27017/"
    export RETRIEVE_MONGO_DB="dserver"
    export RETRIEVE_MONGO_COLLECTION="datasets"


Testing
^^^^^^^

Testing requires a minimal ``dserver`` installation including a
functional search plugin, i.e.

.. code-block:: bash

    pip install dserver
    pip install dserver-search-plugin-mongo

Run tests from within repository root with ``pytest``.
