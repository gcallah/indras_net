#!/bin/sh
if [ -z "$1" ]
  then
    echo "You must provide the location of your Indra repo."
    exit 1
fi
docker rm indra || true
docker run -it -p 8000:8000 -v $1:/home/IndrasNet --name indra gcallah/indra:v6 bash
