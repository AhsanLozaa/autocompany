#!/bin/bash

# Add execute permission to the script
chmod +x "$0"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Apply database migration
python3 manage.py migrate

# Create superuser with automated input
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')" | python3 manage.py shell

# Run the Django development server
# python3 manage.py runserver

# Deactivate virtual environment
# deactivate
