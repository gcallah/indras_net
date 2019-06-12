import os
import tempfile
import json
import pytest
from flask_restplus import Resource, Api, fields
from flask_app import app, HelloWorld

# @pytest.fixture
# def client():
#     db_fd, flask_app.app.config['DATABASE'] = tempfile.mkstemp()
#     flask_app.app.config['TESTING'] = True
#     client = flask_app.app.test_client()
#
#     with flask_app.app.app_context():
#         flask_app.init_db()
#
#     yield client
#
#     os.close(db_fd)
#     os.unlink(flask_app.app.config['DATABASE'])

@pytest.fixture
def client(request):
    test_client = app.test_client()

    def teardown():
        pass

    request.addfinalizer(teardown)
    return test_client


class HelloworldTest(Resource):
    def test_get(client):
        rv = client.HelloWorld.get()
        assert rv == "hello: world"

