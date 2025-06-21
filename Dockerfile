# Builder stage
FROM python:3.12-alpine3.20 AS builder

ENV PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

WORKDIR /nemas

# Copy only requirements first to leverage caching
COPY ./requirements.txt ./requirements.dev.txt /tmp/

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --no-cache postgresql-client && \
    apk add --no-cache --virtual .build-deps build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi && \
    apk del .build-deps && \
    rm -rf /tmp/*

# Copy application code
COPY ./nemas /nemas

# Runtime stage
FROM python:3.12-alpine3.20

ENV PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

WORKDIR /nemas

# Copy virtual environment and app code from builder
COPY --from=builder /py /py
COPY --from=builder /nemas /nemas

# Install runtime dependencies
RUN apk add --no-cache postgresql-client openssl nginx && \
    adduser -D -H -u 1000 django-user && \
    mkdir -p /home/django-user && \
    chown -R django-user:django-user /home/django-user && \
    chown -R django-user:django-user /var/lib/nginx /var/log/nginx /etc/nginx

# Install granian
RUN /py/bin/pip install granian

# Copy Nginx config and set user
COPY ./nginx.conf /etc/nginx/nginx.conf
RUN sed -i 's/user nginx;/user django-user;/g' /etc/nginx/nginx.conf

# Expose ports
EXPOSE 8000 443

# Use entrypoint script to handle cert mounting and start services
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER django-user

# Ensure the /nemas directory is owned by the django-user
RUN chown -R django-user:django-user /nemas
RUN touch /nemas/api_errors.log && \
    chown django-user:django-user /nemas/api_errors.log && \
    chmod 664 /nemas/api_errors.log


CMD ["/entrypoint.sh"]