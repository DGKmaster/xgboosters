from setuptools import setup, find_packages


PACKAGE = "SmartHouse"
NAME = "SmartHouse"
DESCRIPTION = ""
AUTHOR = "sgb"
AUTHOR_EMAIL = ""
URL = ""
VERSION = "1.0.0"
 
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    #long_description=read("releasenotes.txt"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    #package_data=find_package_data(
    #        PACKAGE,
    #        only_in_packages=False
    #  ),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False,
)
