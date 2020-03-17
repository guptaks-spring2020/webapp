#!/usr/bin/env bash
cd /home/ubuntu/
pip3 install -r ../requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate