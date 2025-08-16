#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

uvicorn asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 3 \
  --log-level info \
  --timeout-keep-alive 5
