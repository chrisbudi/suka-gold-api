
# Wait for certs to be available if HTTPS is enabled
if [ "$USE_HTTPS" = "true" ]; then
  while [ ! -f /etc/letsencrypt/live/nemas.id/fullchain.pem ]; do
    echo "Waiting for SSL certificates..."
    sleep 2
  done
fi

# Start Nginx
nginx

# Start Granian with or without HTTPS
if [ "$USE_HTTPS" = "true" ]; then
  granian --interface asginl --host 0.0.0.0 --ssl-certificate /etc/letsencrypt/live/nemas.id/fullchain.pem --ssl-keyfile /etc/letsencrypt/live/nemas.id/privkey.pem --port 8000 app.asgi:application
else
  granian --interface asginl --host 0.0.0.0 --port 8000 --reload app.asgi:application
fi