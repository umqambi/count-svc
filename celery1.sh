#!/bin/sh
exec celery -A app.celery worker  --loglevel=info