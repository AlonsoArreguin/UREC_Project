# UREC Project

UREC Risk Management System

## Create virtual environment & install dependencies

Ensure Python is installed on your system. Windows users are recommended to use Windows Terminal or an IDE.

`python -m venv .venv`  

Linux:  
`. .venv/bin/activate`  
Windows:  
`. .venv\Scripts\activate`

`python -m pip install --upgrade -r requirements.txt`

## Create database *(before first run only)*

`python manage.py migrate`

## Populate default facilities and locations *(recommended)*

`python manage.py loaddata default_locations`

*Currently set to test data. Skipping this step will require you to manually enter facilities and locations through the admin site.*

## Create superuser *(recommended)*

`python manage.py createsuperuser`

## Run server

`python manage.py runserver`