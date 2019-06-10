#!/bin/bash
# This runs on the production server: fetches new code,
# installs needed packages, and restarts the server.

# get new source code onto the server
git pull origin master
# activate our virtual env:
source /home/indrasnet/.virtualenvs/django2/bin/activate
# install all of our packages:
pip install -r docker/requirements.txt
echo "Going to reboot the webserver"
API_TOKEN=14ca851554fc716c30e031b0583fb7e64e05e0db pa_reload_webapp.py indrasnet.pythonanywhere.com
touch reboot
