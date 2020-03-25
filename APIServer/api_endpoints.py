# Indra API server
import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_restplus import Resource, Api, fields

from APIServer.model_creator_api import get_model_creator
from APIServer.model_creator_api import put_model_creator
from APIServer.models_api import get_models
from APIServer.props_api import get_props, put_props
from APIServer.run_model_api import run_model_put
from indra.user import APIUser

app = Flask(__name__)
CORS(app)
api = Api(app)

user = APIUser("Dennis", None)

# the hard-coded dir is needed for Python Anywhere, until
# we figure out how to get the env var set there.
indra_dir = os.getenv("INDRA_HOME", "/home/indrasnet/indras_net")


@api.route('/test')
class Test(Resource):
    def get(self):
        """
        A trivial endpoint just to demo adding something.
        """
        return {'hello': 'susanna'}


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        """
        A trivial endpoint just to see if we are running at all.
        """
        return {'hello': 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    def get(self):
        """
        List our endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


group_fields = api.model("group", {
    "group_name": fields.String,
    "num_of_agents": fields.Integer,
    "color": fields.String,
    "group_actions": fields.List(fields.String),
})

# env_width/height must be >0 when adding agents
create_model_spec = api.model("model_specification", {
    "model_name": fields.String("Enter model name."),
    "env_width": fields.Integer("Enter environment width."),
    "env_height": fields.Integer("Enter environment height."),
    "groups": fields.List(fields.Nested(group_fields)),
})


@api.route('/model_creator')
class ModelCreator(Resource):
    def get(self):
        """
        Returns a description of the model creator interface.
        """
        return get_model_creator()

    @api.expect(create_model_spec)
    def put(self):
        """
        Put a model creation description to create a new model.
        """
        return put_model_creator(api.payload)


@api.route('/models')
class Models(Resource):
    def get(self):
        """
        Get a list of pre-existing models available through the API.
        """
        return get_models(indra_dir)


props = api.model("props", {
    "props": fields.String("Enter propargs.")
})


@api.route('/models/props/<int:model_id>')
class Props(Resource):
    global indra_dir

    def get(self, model_id):
        """
        Get the list of properties (parameters) for a model.
        """
        return get_props(model_id, indra_dir)

    @api.expect(props)
    def put(self, model_id):
        """
        Put a revised list of properties (parameters) for a model
        back to the server.
        """
        return put_props(model_id, api.payload, indra_dir)


@api.route('/models/menu/')
class ModelMenu(Resource):
    global user

    def get(self):
        """
        Get the menu used once into a model.
        """
        return user()


env = api.model("env", {
    "env": fields.String("Should be json rep of env.")
})


@api.route('/models/menu/run/<int:run_time>')
class RunModel(Resource):
    @api.expect(env)
    def put(self, run_time):
        """
        Put a model env to the server and run it `run_time` periods.
        """
        return run_model_put(api.payload, run_time)


if __name__ == "__main__":
    logging.warning("Warning: you should use api.sh to run the server.")
    app.run(host="127.0.0.1", port=8000, debug=True)
