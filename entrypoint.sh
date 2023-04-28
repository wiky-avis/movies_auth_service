#!/bin/bash

# Start server
echo "Starting server"
gunicorn --worker-class=gevent --workers=4 -b ${HTTP_HOST}:${HTTP_PORT} app:app