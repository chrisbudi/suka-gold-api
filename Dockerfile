FROM python:3.12-alpine3.20

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app
EXPOSE 7000

ARG DEV=false


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-dev \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi && \
    rm -rf /tmp && \
    apk del .tmp-build-dev && \
    adduser \
    --disabled-password \
    --home /home/django-user \
    --gecos "" \
    django-user && \
    mkdir -p /home/django-user && \
    chown -R django-user:django-user /home/django-user


ENV PATH "/py/bin:$PATH"

USER django-user
