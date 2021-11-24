#!/usr/bin/env bash

set -e
set -x

cd anton

pytest --capture=no --log-cli-level=ERROR
