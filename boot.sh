#!/bin/sh
source venv/bin/activate
/usr/local/bin/gunicorn --workers=8 --timeout=600 --bind 0.0.0.0:8000 --chdir=/app