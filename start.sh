#!/bin/sh
gunicorn -c config.py wsgi:app