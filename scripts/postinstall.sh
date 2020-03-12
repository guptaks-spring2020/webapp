#!/usr/bin/env bash
cd /home/ubuntu/
python3 -m venv env
#source env/bin/activate
python3 manage.py makemigrations
python3 manage.py migrate