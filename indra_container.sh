#!/bin/sh
docker rm indra || true
docker run -it -p 8000:8000 -v $PWD:/home/IndrasNet indra bash
