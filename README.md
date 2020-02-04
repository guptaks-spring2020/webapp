# Bill Management Application



## Built with:

1. **pip** - package-management system used to install and manage software packages written in Python

2. Python 3.7.6 - Programming Language

3. Django - Django is a Python-based free and open-source web framework, which follows the model-template-view architectural pattern.

4. Postgres - Open-Source Relational Database Management System

5. git - Free and Open-Source distributed version control system


## External Tools Used:
Postman: API Development Environment

## Build and deploy instructions for web application:
- Create your own fork the repository
- Download the zip or clone from the fork
- Unzip the file if you downloaded one
- Open the terminal/command prompt and change directory(cd) to the project's root directory
and the following commands in terminal:



#### Setup virtual environment
  
$ python3 -m venv env
$ source env/bin/activate

#### Install django
  
$ pip install django

#### Install django rest framework

$ pip install djangorestframework

#### Install psycopg2

$ pip install psycopg2


#### Install bcrypt

$ pip install bcrypt==3.1.7

#### Setup Database

$ sudo apt-get update
$ sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contri
$ sudo su - postgres
$ psql
$ CREATE DATABASE myproject;
$ CREATE USER myprojectuser WITH PASSWORD 'password';
$ ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
$ ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
$ ALTER ROLE myprojectuser SET timezone TO 'UTC';
$ GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
$ \q
$ exit

#### Run Application
$ python manage.py runserver

#### Run Test Cases
$ python3 manage.py test account.tests

### To contribute
- Create a branch using
$ git checkout -b <branch name>

$ git push origin <branch name>

- Create a new PR against the upstream and wait for the approval of the PR

#test