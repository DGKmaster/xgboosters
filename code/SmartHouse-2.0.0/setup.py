

from setuptools import setup, find_packages

PACKAGE = "SmartHouse"
NAME = "smarthouse"
DESCRIPTION = ""
AUTHOR = "sgb"
AUTHOR_EMAIL = ""
URL = ""
VERSION = "2.0.0"
 
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    #long_description=releasenotes,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    zip_safe=False,
)

