# Indra API server
import os
from flask import Flask
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
import json
from indra.user import APIUser
from models.run_dict_helper import setup_dict
from indra.agent import AgentEncoder
from indra.env import Env
# these imports must be automated somehow;
# also, keep name constant and preface with model name, e.g.,
# fashion.unrestorable()
from models.sandpile import sp_unrestorable
from models.bacteria import bt_unrestorable
from models.bigbox import bb_unrestorable
from models.fashion import fs_unrestorable
from models.flocking import fl_unrestorable
from models.fmarket import fm_unrestorable
from models.segregation import sg_unrestorable
from models.wolfsheep import ws_unrestorable
from models.gameoflife import gl_unrestorable


ERROR = "Error:"

app = Flask(__name__)
CORS(app)
api = Api(app)

user = APIUser("Dennis", None)

indra_dir = os.getenv("INDRA_HOME", "/home/indrasnet/indras_net")


def err_return(s):
    return {ERROR: s}


def load_models():
    model_file = indra_dir + "/models/models.json"
    with open(model_file) as file:
        return json.loads(file.read())["models_database"]


def load_menu():
    menu_file = indra_dir + "/indra/menu.json"
    with open(menu_file) as file:
        return json.loads(file.read())["menu_database"]


def json_converter(object):
    return json.loads(json.dumps(object.to_json(),
                      cls=AgentEncoder, indent=4))


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


model_specification = api.model("model_specification", {
    "model_name": fields.String("Enter model name."),
    "groups": fields.List(fields.String("Enter group names"))
})


@api.route('/model_creator')
class ModelCreator(Resource):
    def get(self):
        return {'feature_name':
                'This is the URL for the model creator: '
                + 'it is used with a PUT request.'}

    @api.expect(model_specification)
    def put(self):
        model_features = api.payload
        return json_converter(Env(model_features["model_name"]))


@api.route('/models')
class Models(Resource):
    def get(self):
        global indra_dir

        try:
            models_db = load_models()
        except FileNotFoundError:
            return err_return("Model file not found.")

        models_response = []
        for model in models_db:
            doc = ""
            if "doc" in model:
                doc = model["doc"]
            models_response.append({"model ID": model["model ID"],
                                    "name": model["name"],
                                    "doc": doc,
                                    "source": model["source"]})
        return models_response


props = api.model("props", {
    "props": fields.String("Enter propargs.")
})


@api.route('/models/props/<int:model_id>')
class Props(Resource):
    global indra_dir

    def get(self, model_id):
        try:
            models_db = load_models()
            with open(indra_dir + "/" + models_db[model_id]["props"]) as file:
                model_prop = json.loads(file.read())
                return model_prop
        except (IndexError, KeyError, ValueError):
            return err_return("Invalid model id " + str(model_id))
        except FileNotFoundError:
            return err_return("Models or props file not found")

    @api.expect(props)
    def put(self, model_id):
        props_dict = api.payload
        models_db = load_models()
        con_env = 0
        ret = setup_dict[models_db[model_id]["run"]](props=props_dict)
        env = ret[con_env]
        return json_converter(env)


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
