#!/bin/sh

docker run --rm -it -p 3000:3000 -v `pwd`/webapp/public:/home/public -v `pwd`/webapp/src:/home/src --name webapp-dev-container gcallah/indras_webapp sh
