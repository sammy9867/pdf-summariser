#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

# Wait for postgres to be ready
./scripts/entrypoint.sh postgres_ready

# Run migrations
python3 manage.py migrate

# Start Django development server with auto-reload enabled
python3 manage.py runserver 0.0.0.0:8000
