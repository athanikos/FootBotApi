import setuptools

import FootBotApi
from distutils.core import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='FootBotApi',
    version="0.0.1",
    license='Apache Software License',
    author='Nikos Athanasakis',
    packages=setuptools.find_packages(),
    author_email='athanikos@gmail.com',
    description='A set of rest api methods used for calculating statistics and applying models for football data ',
    tests_require=['pytest'],
    classifiers=[
        "Development Status:: 2 - Pre - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
