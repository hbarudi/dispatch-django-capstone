Setup (Development)
===================

Virtual environment
-------------------

Create and activate a virtual environment, then install dependencies::

   python -m venv .venv
   .\.venv\Scripts\activate
   python -m pip install -r requirements.txt

Database
--------

This project is configured to use MariaDB. Create a database and update your local
database credentials in the Django settings file.

Migrations and running
----------------------

Run migrations and start the development server::

   python manage.py migrate
   python manage.py runserver 8001

Tests
-----

Run the automated tests::

   python manage.py test dispatch_app.unit_tests

