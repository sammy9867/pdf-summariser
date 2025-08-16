#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

# Run migrations
python3 manage.py migrate

# Gets the directory where this script resides and moves one level up
cd "$(dirname "$0")/.."

# Start uvicorn server
uvicorn asgi:application --host 0.0.0.0 --port 8000 --reload
