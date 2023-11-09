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

## Create superuser *(recommended)*

`python manage.py createsuperuser`

## Run server

`python manage.py runserver`