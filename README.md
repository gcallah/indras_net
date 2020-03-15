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

To run tests on Python code, run `make pytests`. To run tests on JavaScript
code, run `make jstests`. To run tests on both Python and JavaScript code,
run `make tests`. These can be run inside or outside the Docker container.
Optionally, you can first `cd` into [APIServer](APIServer), [indra](indra),
[models](models), or [webapp](webapp) before running `make tests` to run only
the tests for that directory.

To test the APIServer with the front end locally:

- Back end:
    - `cd` into [APIServer](APIServer) and run `./api.sh` to start the server.
- Front end:
    - Run `make setup_react` to install all modules listed as dependencies.
    - Within each file in `webapp/src/components/`, find and replace
      `https://indrasnet.pythonanywhere.com/` with your server's address (which
      should be `http://127.0.0.1:8000` if you ran `api.sh` above).
    - `cd` into [webapp](webapp) and run `npm run start`.
    - To open test coverage of Front End in your browser, `cd` into [webapp](webapp) and run `npm run coverage`.

If `ImportError: bad magic number in 'config': b'\x03\xf3\r\n'` occurs, please try to run `find . -name \*.pyc -delete` .

Work in Progress
----------------

Trying to get all the models working from the API server. 

Flocking:
Using Windows Subsystem for Linux(WSL), on Ubuntu 18.04, entering the iPython terminal through the "Examine Model Data" option in the Flocking menu and entering `user.env` to check environment values returns an error with `printer.pretty(obj)`. This occurs with all other models. Need other people to try and replicate this error. Entering user, or any of the other properties like `.menu` or `.user_msgs` do not return any errors.

Selecting the Matplotlib options (Population Graph, Scatter Plot, etc) in the model menus return nothing. No graphs can be seen. Current theory is that matplotlib is not configured correctly on WSL. To get around this, you can use a Windows X-Server like Xming, and add `export DISPLAY=localhost:0.0` to your login script. This will allow the matplotlib graphs to show in an external window. 

Still need to figure out how to have small groups/flocks gather together into a single flock. (Idea: treat each mini-flock as an agent and draw borders, to which we apply `bird_action()` to each triangular point of the mini-flock, making sure mini flocks form a proper flock? )

With regard to the Kanban board: 
1) I have not been able to replicate this problem at all with single birds. However small groups/flocks will stop moving the moment all the birds have joined a group/flock. This seems like intended behavior, but the next step is to have these small flocks gather together to make a single flock. 
2) Also have not been able to replicate this. It seems like the distance checking has been already fixed.
3) All the tests have been updated. However, `test_bird_action()`, the most important one, currently is using an inelegant solution to test `bird_action()` because of an odd problem with agent properties. I've left comments on `test_bird_action()` as a sort of TO DO or reminder.
4) Documentation still needs to be written.
5) Need to see if the model works on APIServer.
6) Haven't figured out how to orient markers yet. 

Frontend:
Dark mode currently does not change the colors of components, such as the header or buttons.
Mobile design has not been implememnted. We had planned on having the carousel image be below the menu items.
The general layout could be structured a little better. Especially on the action menu page. There is a lot of white space that is not being utilized and the alignment of things like the header, the title, and menu items are inconsistent.
There are some unused component files that should be removed.
A lot of testing needs to be implemented.