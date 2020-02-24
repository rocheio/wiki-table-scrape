#!/bin/sh
set -e

if [ ! -f venv/ ]; then
    python3 -m venv venv
fi

. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt -r requirements_dev.txt

# Lint with flake8
# stop the build if there are Python syntax errors or undefined names
flake8 wikitablescrape \
    --max-complexity=15 \
    --max-line-length=100

# Run unit tests and code coverage checks
coverage run --source wikitablescrape -m unittest discover
coverage report --fail-under=80
