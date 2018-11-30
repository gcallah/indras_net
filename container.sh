#!/bin/sh
echo "Going to remove any lingering indra container."
docker rm indra 2> /dev/null || true
echo "Now running docker to spin up the container."
docker run -it -p 8000:8000 -v $PWD:/home/IndrasNet indra bash
