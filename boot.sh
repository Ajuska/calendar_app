#!/bin/sh
source __venv__/bin/activate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - calendar_app:app
