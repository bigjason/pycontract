from os import path
from setuptools import setup, find_packages

from pycontract import VERSION

with open(path.join(path.dirname(__file__), 'README.txt')) as f:
    readme = f.read()


setup(
    name="pycontract",
    version=".".join(map(str, VERSION)),
    description="pycontracts is a  data contracts container for python.",
    long_description=readme,
    author="Jason Webb",
    author_email="bigjasonwebb@gmail.com",
    packages=find_packages(),
    include_package_data=True
)
