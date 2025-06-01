#!/usr/bin/env python3
"""
Setup script for Gemini Engineer
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="gemini-engineer",
    version="1.0.0",
    author="Gemini Engineer Team",
    description="AI-driven terminal application for software engineering assistance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gemini-engineer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.11",
    install_requires=[
        "google-generativeai>=0.3.0",
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "gemini-engineer=main:main",
        ],
    },
    keywords="ai, coding, assistant, gemini, terminal, cli",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/gemini-engineer/issues",
        "Source": "https://github.com/yourusername/gemini-engineer",
    },
) 