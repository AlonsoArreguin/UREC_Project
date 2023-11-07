# UREC_Project
UREC Risk Management System.
Build & Run:
// create virtual environment & install dependencies
python -m venv .
env\Scripts\activate
python -m pip install Django
python -m pip install Pillow

// run server
python manage.py runserver

// when you are running the server for the first time you
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
