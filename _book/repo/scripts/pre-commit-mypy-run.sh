#!/usr/bin/env bash

# taken from: https://jaredkhan.com/blog/mypy-pre-commit

# A script for running mypy,
# with all its dependencies installed.

set -o errexit

# Change directory to the project root directory.
cd "$(dirname "$0")"/..

pip uninstall ag2 --yes --quiet

pip install -q -e .[types]

mypy
