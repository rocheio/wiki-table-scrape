#!/bin/sh
set -e

if [ ! -f venv/ ]; then
    python3 -m venv venv
fi

. venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt

coverage run --source wikitablescrape -m unittest discover
coverage report --fail-under=80

rm -rf build/ dist/
python setup.py sdist bdist_wheel

if [ ! -f ~/.pypirc ]; then
    echo "need to populate your '~/.pypirc' file with credentials for twine"
fi

twine upload dist/*
