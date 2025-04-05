#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install the dependencies
pip install -r requirements.txt

# Collect the static files
python manage.py collectstatic --no-input

# Miagrate the database data
python3 manage.py makemigrations
python manage.py migrate

# Create the super user
python manage.py createsu