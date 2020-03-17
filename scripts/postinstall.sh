#!/usr/bin/env bash
cd /home/ubuntu/
pip install -r ../requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate