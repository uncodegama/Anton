#!/usr/bin/env bash

set -e
set -x

cd anton

pytest --show-capture=no
