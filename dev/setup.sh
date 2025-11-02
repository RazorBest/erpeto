#!/bin/bash
set -e

PARENT_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
VENV_HTTP_APPS=".venv_http_apps"


# TODO: make sure the script is run from a specific place

# Create venv if it doesn't exist
if [ ! -d "$VENV_HTTP_APPS" ]; then
    echo Creating virtual environment in $VENV_HTTP_APPS...
    python3 -m virtualenv "$VENV_HTTP_APPS"
fi

# Activate venv
echo Activating virtual environment $VENV_HTTP_APPS...
# shellcheck disable=SC1091
source "$VENV_HTTP_APPS/bin/activate"

echo Installing dependencies...
pip install --upgrade pip
pip install -r $PARENT_PATH/requirements-http-apps.txt

echo Done
