import os
import re

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with open(os.path.join(here, *parts), encoding="utf-8") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


readme = read("README.md")
version = find_version("lightnode", "__init__.py")
github_url = "https://github.com/zhangwm404/quorum-lightnode-py"

setup(
    name="quorum-lightnode",
    version=version,
    url=github_url,
    license="MIT",
    author="zhangwm404",
    author_email="zhangwm404@gmail.com",
    description="quorum lightnode for python",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "example"]),
    platforms="any",
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "eth_keys",
        "pycryptodome",
        "protobuf",
        "dataclasses-json",
    ],
    extras_require={
        "dev": [
            "pytest>=3",
            "coverage",
            "tox",
            "twine",
            "pylint",
            "pylint-protobuf",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
