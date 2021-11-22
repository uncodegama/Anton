#!/usr/bin/env bash

set -e
set -x

tree
pwd
cd ..
pwd
cd anton

pytest
