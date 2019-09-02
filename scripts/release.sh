#!/bin/sh
set -e

. venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt

coverage run --source wikitablescrape -m unittest discover
coverage report --fail-under=80

python setup.py sdist bdist_wheel
