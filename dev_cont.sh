#!/bin/sh
export HOST_PORT="8000"
export REPO=indras_net
export PROJECT=IndrasNet
if [ $1 ]
then
    HOST_PORT=$1
fi

echo "Going to remove any lingering indra-dev container."
docker rm indra-dev 2> /dev/null || true
echo "Now running docker to spin up the container."
docker run -it -p $HOST_PORT:8000 -v $PWD:/home/$PROJECT gcallah/$REPO-dev bash
