# Indra API server
import os
from flask import Flask
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
import json
from indra.user import APIUser
from models.run_dict import setup_dict
from models.run_dict import rdict
from indra.agent import AgentEncoder


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
    return json.dumps(object.to_json(), cls=AgentEncoder, indent=4)


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


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
                                    "doc": doc})
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
        env = setup_dict[models_db[model_id]["run"]](props=props_dict)[0]
        return json_converter(env)


@api.route("/models/menu/")
class ModelMenu(Resource):
    global user

    def get(self):
        return user()


@api.route("/models/menu/<int:model_id>/<int:menu_id>")
class MenuItem(Resource):
    global user

    def put(self, model_id, menu_id):
        models_db = load_models()
        if 0 <= menu_id < 6 and (type(menu_id) is int):
            try:
                user.tell("execute menu item" + str(menu_id))
                user.tell(str(load_menu()))
                env = rdict[models_db[model_id]["run"]](menu_id)[0]
                return json_converter(env)
            except TypeError:
                return 'not running the model'
        else:
            return err_return("Invalid menu id " + str(menu_id))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
