#!/bin/bash
# This script must be run from the project's root directory

set -e
set -o pipefail

export NO_COLOR=false
export PYTEST_ADDOPTS="--color=yes"

args="$@"
if [ "${args}" = "" ]; then
    args="isort black pylint mypy pytest"
fi

for var in $args; do
    if [ "${var}" = "isort" ]; then
        python3 -m isort -c cdprecorder/
    elif [ "${var}" = "black" ]; then
        python3 -m black --line-length 120 --check cdprecorder/
    elif [ "${var}" = "pylint" ]; then
        python3 -m pylint --output-format=colorized cdprecorder/
    elif [ "${var}" = "mypy" ]; then
        python3 -m mypy cdprecorder/
    elif [ "${var}" = "pytest" ]; then
        python3 -m pytest --cov=cdprecorder tests
    else
        echo ${var}: Unkown check option
    fi
    #echo "$var"
done
