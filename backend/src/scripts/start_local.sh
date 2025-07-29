#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

# Run migrations
python3 manage.py migrate

# Start Django development server
python3 manage.py runserver 0.0.0.0:8000
