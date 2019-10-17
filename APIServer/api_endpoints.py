# Indra API server
import os
from flask import Flask
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
import json
from indra.user import APIUser
from indra.env import Env
from APIServer.props_api import get_props, put_props
from APIServer.models_api import get_models
from APIServer.model_creator_api import put_model_creator
from APIServer.model_creator_api import get_model_creator
from APIServer.api_utils import json_converter
# these imports below must be automated somehow;
# also, these things are unserializable, NOT unrestorable!
# (Otherwise why bother?)
# also, keep name constant and preface with model name, e.g.,
# fashion[unserializable()]
from models.sandpile import sp_unrestorable
from models.bacteria import bt_unrestorable
from models.bigbox import bb_unrestorable
from models.fashion import fs_unrestorable
from models.flocking import fl_unrestorable
from models.fmarket import fm_unrestorable
from models.segregation import sg_unrestorable
from models.wolfsheep import ws_unrestorable
from models.gameoflife import gl_unrestorable


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
    "group_name": fields.List(fields.String)
})

create_model_spec = api.model("model_specification", {
    "model_name": fields.String("Enter model name."),
    "env_width": fields.Integer("Enter enviornment width."),  # can't be 0
    "env_height": fields.Integer("Enter enviornment height."),  # can't be 0
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
class Run(Resource):
    global user

    @api.expect(props)
    def put(self, run_time):
        env_json = api.payload
        v = Env(name='API env', serial_obj=env_json)
        # this should be dictionary lookup not if elif statements.
        if v.name == "Sandpile":
            sp_unrestorable(v)
        elif v.name == "Petrie dish":
            bt_unrestorable(v)
        elif v.name == "Town":
            bb_unrestorable(v)
        elif v.name == "Society":
            fs_unrestorable(v)
        elif v.name == "the_sky":
            fl_unrestorable(v)
        elif v.name == "fmarket":
            fm_unrestorable(v)
        elif v.name == "A city":
            sg_unrestorable(v)
        elif v.name == "meadow":
            ws_unrestorable(v)
        elif v.name == "Game of Life":
            gl_unrestorable(v)
        v.runN(periods=run_time)
        return json_converter(v)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
