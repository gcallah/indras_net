#!/bin/sh
docker rm indra 2> /dev/null || true
docker run -it -p 8000:8000 -v $PWD:/home/IndrasNet indra bash
