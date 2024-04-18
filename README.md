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

## Populate default groups *(recommended)*

`python manage.py loaddata default_groups`

*New staff users will default to having no permissions, making them effectively useless on the admin site. Skipping this step will require manual group creation to give new staff permissions.*

## Manually populate site domain *(required for deployment)*

On the admin site, go to Sites and change the default `example.com` site to whatever the domain name of the site will be. For testing purposes, the domain can be set to `http://127.0.0.1:8000`. *Failing to set this value will result in incorrect links inside email notifications.*

## Create superuser *(recommended)*

`python manage.py createsuperuser`

## Run server

`python manage.py runserver`