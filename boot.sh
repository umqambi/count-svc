#!/bin/sh
flask db upgrade
exec gunicorn -b :5500 --access-logfile - --error-logfile - count-svc:app