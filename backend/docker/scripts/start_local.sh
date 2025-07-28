#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

# TODO: Switch between local/test/prod and handle hosted mount
# Run migrations
python3 src/manage.py migrate

# Start Django development server
python3 src/manage.py runserver 0.0.0.0:8000
