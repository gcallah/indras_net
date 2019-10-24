# Indra API server
import os
from flask import Flask
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
import json
from indra.user import APIUser
from APIServer.props_api import get_props, put_props
from APIServer.models_api import get_models
from APIServer.run_model_api import run_model_put
from APIServer.model_creator_api import put_model_creator
from APIServer.model_creator_api import get_model_creator


app = Flask(__name__)
CORS(app)
api = Api(app)

user = APIUser("Dennis", None)

indra_dir = os.getenv("INDRA_HOME", "/home/indrasnet/indras_net")


def load_menu():
    menu_file = indra_dir + "/indra/menu.json"
    with open(menu_file) as file:
        return json.loads(file.read())["menu_database"]


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


group_fields = api.model("group", {
    "group_name": fields.String,
    "num_of_agents": fields.Integer,
    "color": fields.String,
})

# env_width/height must be >0 when adding agents
create_model_spec = api.model("model_specification", {
    "model_name": fields.String("Enter model name."),
    "env_width": fields.Integer("Enter enviornment width."),
    "env_height": fields.Integer("Enter enviornment height."),
    "groups": fields.List(fields.Nested(group_fields)),
})


@api.route('/model_creator')
class ModelCreator(Resource):
    def get(self):
        return get_model_creator()

    @api.expect(create_model_spec)
    def put(self):
        return put_model_creator(api.payload)


@api.route('/models')
class Models(Resource):
    def get(self):
        return get_models(indra_dir)


props = api.model("props", {
    "props": fields.String("Enter propargs.")
})


@api.route('/models/props/<int:model_id>')
class Props(Resource):
    global indra_dir

    def get(self, model_id):
        return get_props(model_id, indra_dir)

    @api.expect(props)
    def put(self, model_id):
        return put_props(model_id, api.payload, indra_dir)


@api.route("/models/menu/")
class ModelMenu(Resource):
    global user

    def get(self):
        return user()


@api.route("/models/menu/run/<int:run_time>")
class RunModel(Resource):
    @api.expect(props)
    def put(self, run_time):
        return run_model_put(api.payload, run_time)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
