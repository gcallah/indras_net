#!/bin/bash
# for the production server: fetches new code,
# installs needed packages, and restarts the server.

# get new source code
git pull origin master
# activate our virtual env:
source /home/indrasnet/.virtualenvs/django2/bin/activate
# install all of our packages:
pip install -r docker/requirements.txt
echo "going to reboot the webserver"
touch /var/www/indrasnet_pythonanywhere_com_wsgi.py
