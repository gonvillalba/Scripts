#!/bin/bash

# Run migrations
docker-compose exec web python manage.py migrate

# Import dummy data
docker-compose exec web python create_dummy_data.py
