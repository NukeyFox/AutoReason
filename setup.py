import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "AutoReason",
    version = "0.0.1",
    author = "Johanan Lee Mahendran",
    author_email = "jl2192@cantab.com",
    description = ("Tools for Automated Reasoning"),
    license = "MIT",
    keywords = "automated reaosning",
    url = "https://github.com/NukeyFox/AutoReason",
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)