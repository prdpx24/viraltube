#!/bin/bash
echo "Starting build process........."
echo "Checking python3.7"
if ! [ -x "$(command -v python3.7)" ]; then
    echo "Installing python3.7"
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3-pip python3.7 python3.7-dev
else
    echo "Python3.7 Exists"
fi


echo "Checking redis-server..."
if ! [ -x "$(command -v redis-server)" ]; then
    echo 'Installing redis-server' >&2
    sudo apt install redis-server
else
    echo "redis-server exists!"
fi
echo "Starting redis-server in background"
redis-server --daemonize yes

echo "Installing virtualenv"
sudo pip3 install virtualenv

echo "Creating virtualenv in $PWD"
virtualenv .venv --python=/usr/bin/python3.7
source ./.venv/bin/activate
echo "Installing dependencies"
pip install -r requirements.txt
echo "Running migrations"
python manage.py makemigrations
python manage.py migrate

echo "Running django collectstatic"
python manage.py collectstatic --no-input

echo "Starting celery beat in background"
celery -A tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

echo "Starting celery worker in background"
celery -A tasks worker -l info &

echo "Starting django server"
python manage.py runserver 8000
