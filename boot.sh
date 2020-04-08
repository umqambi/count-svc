#!/bin/sh
exec gunicorn -b :5500 --access-logfile - --error-logfile - count-svc:app