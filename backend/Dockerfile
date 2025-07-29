FROM python:3.13-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_VERSION=25.1.1 \
    APP_DIR=/usr/src/pdf_summariser

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        gettext \
        git \
        libpq-dev \
        locales && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install pip==${PIP_VERSION}

# ---- Dependency layer ----
FROM base AS dependencies

COPY src/requirements/ ${APP_DIR}/requirements/

RUN pip install -r ${APP_DIR}/requirements/prod.txt

# ---- Final layer ----
FROM dependencies AS artifact

COPY src/ ${APP_DIR}/

WORKDIR ${APP_DIR}

RUN chmod +x scripts/start.sh

RUN python manage.py collectstatic --no-input

CMD ["scripts/start.sh"]
