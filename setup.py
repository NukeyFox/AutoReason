import os
from setuptools import setup, find_packages
import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "autoreason.core.example",  # Full module name
        ["autoreason/core/example.cpp"],  # Path to the C++ source file
        include_dirs=[pybind11.get_include()],  # Include pybind11 headers
        language="c++",
    ),
]

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "autoreason",
    version = "0.0.2",
    author = "Johanan Lee Mahendran",
    author_email = "jl2192@cantab.ac.uk",
    description = ("Tools for Automated Reasoning"),
    license = "MIT",
    keywords = "automated reasoning",
    url = "https://github.com/NukeyFox/AutoReason",
    packages=find_packages(),
    long_description=read('README.md'),
    setup_requires=[],
    install_requires=["lark"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)