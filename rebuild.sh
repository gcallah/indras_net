#!/bin/bash
# for the production server: fetches new code,
# installs needed packages, and restarts the server.

git pull origin master
source /home/indrasnet/.virtualenvs/django2/bin/activate
pip install -r docker/requirements.txt
echo "going to reboot the webserver"
touch /var/www/indrasnet_pythonanywhere_com_wsgi.py
