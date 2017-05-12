#!/usr/bin/env bash

set -ue
set -o pipefail

name=$(basename $0)

echo 'into install.sh'
yum install
pip install -Ur requirements.txt