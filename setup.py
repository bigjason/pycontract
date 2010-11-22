from os import path
from setuptools import setup, find_packages

from pycontract import VERSION

with open(path.join(path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()


setup(
    name="pycontract",
    version=".".join(map(str, VERSION)),
    license="MIT",
    description="A data contracts system for python loosly modeled after django forms.",
    long_description=readme,
    url="https://github.com/bigjason/pycontract",
    author="Jason Webb",
    author_email="bigjasonwebb@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
       "Development Status :: 3 - Alpha",
       "Operating System :: OS Independent",
       "License :: OSI Approved :: MIT License",
       "Intended Audience :: Developers",
       "Programming Language :: Python :: 2.7"
    ],
    install_requires = [
        "python-dateutil"                        
    ]
)
