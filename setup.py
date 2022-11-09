from setuptools import setup

url = ""
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="dtool-lookup-server-retrieve-mongo-plugin",
    packages=["dtool_lookup_server_retrieve_mongo_plugin"],
    version=version,
    description="Retrieve plugin for dtool-lookup-server using mongodb",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@gmail.com",
    url=url,
    install_requires=[],
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
