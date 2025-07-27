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

ARG ENVIRONMENT
ENV ENVIRONMENT=${ENVIRONMENT}

COPY src/requirements/ ${APP_DIR}/requirements/

RUN if [ -z "$ENVIRONMENT" ]; then echo "ENVIRONMENT arg is missing!"; exit 1; fi

RUN pip install -r ${APP_DIR}/requirements/${ENVIRONMENT}.txt

# ---- Final layer ----
FROM dependencies AS artifact

COPY src/ docker/scripts/ ${APP_DIR}/

WORKDIR ${APP_DIR}

RUN chmod +x start_local.sh start.sh

RUN python manage.py collectstatic --no-input

# TODO: Switch between local and prod
CMD ["./start_local.sh"]
