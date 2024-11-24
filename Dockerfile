# Builder stage
FROM python:3.12-alpine3.20 AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

# Copy requirements files
COPY ./requirements.txt ./requirements.dev.txt /tmp/

# Set working directory
WORKDIR /nemas

# Argument to determine if it's a development build
ARG DEV=true

# Install dependencies and create a virtual environment
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

# Copy application code
COPY ./nemas /nemas

# Runtime stage
FROM python:3.12-alpine3.20

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

# Copy virtual environment from builder stage
COPY --from=builder /py /py

# Copy application code from builder stage
COPY --from=builder /nemas /nemas

# Set working directory
WORKDIR /nemas

# Install runtime dependencies
RUN apk add --update --no-cache postgresql-client openssl nginx && \
    adduser --disabled-password --home /home/django-user --gecos "" django-user && \
    mkdir -p /home/django-user && \
    chown -R django-user:django-user /home/django-user && \
    mkdir -p /etc/ssl/certs /etc/ssl/private && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/selfsigned.key \
    -out /etc/ssl/certs/selfsigned.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=52.221.181.88"

# Install Gunicorn
RUN /py/bin/pip install gunicorn

# Configure Nginx
COPY ./nginx.conf /etc/nginx/nginx.conf

# Ensure Nginx runs as non-root user
RUN sed -i 's/user nginx;/user django-user;/g' /etc/nginx/nginx.conf && \
    chown -R django-user:django-user /var/lib/nginx && \
    chown -R django-user:django-user /var/log/nginx && \
    chown -R django-user:django-user /etc/nginx

# Expose the HTTPS port for Nginx
EXPOSE 8000

# Start Nginx and Gunicorn with HTTPS
CMD ["sh", "-c", "nginx && gunicorn --certfile=/etc/ssl/certs/selfsigned.crt --keyfile=/etc/ssl/private/selfsigned.key --bind 0.0.0.0:8000 --cert-reqs=0 nemas.wsgi:application"]