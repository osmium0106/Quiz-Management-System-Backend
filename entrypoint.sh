#!/bin/bash

# Wait for postgres (skip for Railway)
if [ -n "$DATABASE_URL" ]; then
    echo "Using Railway PostgreSQL DATABASE_URL"
elif [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
    echo "Waiting for postgres..."
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
else
    echo "No database host specified, proceeding..."
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"

# Start server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000