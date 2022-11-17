from setuptools import setup

url = "https://github.com/jic-dtool/dtool-lookup-server-retrieve-plugin-mongo"
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="dtool-lookup-server-retrieve-plugin-mongo",
    packages=["dtool_lookup_server_retrieve_plugin_mongo"],
    version=version,
    description="Retrieve plugin for dtool-lookup-server using mongodb",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@gmail.com",
    url=url,
    install_requires=[
        "pymongo",
        "dtoolcore>=3.18.0",
        "dtool-lookup-server",   # Add version constraints once v1 of dtool-lookup-server-has been released  # NOQA
    ],
    entry_points={
        "dtool_lookup_server.retrieve": [
            "MongoRetrieve=dtool_lookup_server_retrieve_plugin_mongo.utils_retrieve:MongoRetrieve",  # NOQA
        ],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
