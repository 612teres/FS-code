"""
Setup script for FS-Code IDE
Package the application for desktop distribution
"""

from setuptools import setup, find_packages
import sys
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fs-code",
    version="2.0.0",
    author="FABIAN TERES",
    author_email="",
    description="A modern Python IDE with syntax highlighting and tabbed interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fs-code",
    py_modules=["app"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    entry_points={
        "console_scripts": [
            "fs-code=app:main",
        ],
        "gui_scripts": [
            "fs-code-gui=app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
