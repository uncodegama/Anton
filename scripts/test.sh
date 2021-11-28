#!/usr/bin/env bash

set -e
set -x

cd anton

pytest --capture=no --log-cli-level=ERROR --cov=anton --cov-report=html --cov-report=xml --cov-config=./tests/.coveragerc
