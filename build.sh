#!/usr/bin/env bash
# Render build hook. Runs on every deploy.
set -o errexit

echo "==> Installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Collecting static files"
python manage.py collectstatic --no-input

echo "==> Applying database migrations"
python manage.py migrate --no-input

echo "==> Seeding initial content"
python manage.py seed
python manage.py add_gerat
python manage.py fill_all

echo "==> Build finished"
