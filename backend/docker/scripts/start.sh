#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

gunicorn pdf_summariser.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --worker-class sync \
  --timeout 30 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
