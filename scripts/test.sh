#!/bin/sh
set -e

if [ ! -f venv/ ]; then
    python3 -m venv venv
fi

. venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt

# Run unit tests and code coverage checks
coverage run --source wikitablescrape -m unittest discover && coverage report --fail-under=80

# Show coverage data in a browser
coverage html && open htmlcov/index.html
