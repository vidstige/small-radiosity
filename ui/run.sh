#!/bin/sh
set -e
if [ ! -d venv/ ]; then
    python3 -m venv venv
    venv/bin/python3 -m pip install -r requirements.txt
fi
. venv/bin/activate
FLASK_APP=server.py FLASK_DEBUG=1 flask run --reload
