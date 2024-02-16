#!/bin/bash
# This script must be run from the project's root directory

set -e
set -o pipefail

python3 -m isort -c cdprecorder/
python3 -m black --line-length 120 --check cdprecorder/
python3 -m pylint cdprecorder/
python3 -m mypy cdprecorder/
python3 -m pytest --cov=cdprecorder tests

