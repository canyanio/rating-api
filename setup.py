# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="rating-api",
    version="0.1.0",
    author="Canyan Team",
    author_email="dev@canyan.io",
    description="Canyan Rating Engine API",
    long_description=readme,
    long_description_content_type="text/markdown",
    license=license,
    url="https://canyan.io",
    install_requires=[
        "Click>=7.1",
        "fastapi>=0.63",
        "graphene>=2.1.8",
        "motor>=2.3.0",
        "passlib[bcrypt]",
        "uvicorn>=0.13",
    ],
    packages=find_packages(exclude=("tests")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        rating-api=rating_api.main:main_with_env
    """,
)
