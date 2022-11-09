README
======

Retrieve plugin for dtool-lookup-server using mongodb

To install the dtool-lookup-server-retrieve-plugin-mongo package.

.. code-block:: bash

    cd dtool-lookup-server-retrieve-plugin-mongo
    python setup.py install


To configure the connection to the mongo database.

.. code-block:: bash

    export RETRIEVE_MONGO_URI="mongodb://localhost:27017/"
    export RETRIEVE_MONGO_DB="dtool_lookup_server"
    export RETRIEVE_MONGO_COLLECTION="datasets"
