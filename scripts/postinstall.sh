#!/usr/bin/env bash
cd /home/ubuntu/webapp/
python3 manage.py makemigrations
python3 manage.py migrate