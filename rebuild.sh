#!/bin/bash
# for the dev server: fetches new code and restarts the server.

git pull origin master
echo "going to reboot the webserver"
touch /var/www/indrasnet_pythonanywhere_com_wsgi.py
