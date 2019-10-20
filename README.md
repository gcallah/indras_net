[![Build Status](https://travis-ci.org/gcallah/indras_net.svg?branch=master)](https://travis-ci.org/gcallah/indras_net)
[![codecov](https://codecov.io/gh/gcallah/indras_net/branch/master/graph/badge.svg)](https://codecov.io/gh/gcallah/indras_net)

Indra
=====
This is a project building an agent-based modeling system in Python. The
ultimate goal is to build a GUI front-end that will allow non-coders to build
models, while at the same time permitting coders to use Python for more
flexibility in model creation.


We are currently building **indra2**, a new version of the system. Our API
Serever is moving along,  we have a react frontend in progress, and many models
have been ported to version 2.

Developing and Contributing
---------------------------
To configure your system for development, first install Python 3 and git and
then run `make create_dev_env`. This will install some dependencies using PIP.
Follow the outputted instructions for setting your environment variables.

To build the Docker container with the development environment, run
`make dev_container`.

To run the Docker container with the development environment, run
`./dev_cont.sh`.

To run tests, run `make tests`. This can be done inside or outside the Docker
container. Optionally, you can first `cd` into [APIServer](APIServer),
[indra](indra), or [models](models) before running `make tests` to run only the
tests for that directory.
