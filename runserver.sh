#!/bin/sh

export FLASK_APP=APIServer/flask_app
# bind to 0.0.0.0 to be accessible from outside
flask run -h 0.0.0.0 -p 8000
