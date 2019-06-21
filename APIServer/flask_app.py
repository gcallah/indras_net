# Indra API server
import os
from indra.user import APIUser
from flask import Flask
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
import json
from models import basic
from models import fashion, forestfire, sandpile
from models import segregation, wolfsheep

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
    "model ID": fields.Integer,
    "props": fields.String("Enter propargs.")
})


@api.route('/models/props/<int:model_id>')
class Props(Resource):
    global indra_dir

    def get(self, model_id):
        try:
            models_db = load_models()
            with open(indra_dir + "/" + models_db[model_id]["props"]) as file:
                props = json.loads(file.read())
                return props
        except (IndexError, KeyError, ValueError):
            return err_return("Invalid model id " + str(model_id))
        except FileNotFoundError:
            return err_return("Models or props file not found")

    @api.expect(props)
    def put(self, model_id):
        try:
            ret = api.payload
            try:
                props = ret["props"]  # noqa F841
                if model_id == 5:
                    basic.set_up(props)
                elif model_id == 0:
                    fashion.set_up(props)
                elif model_id == 1:
                    forestfire.set_up(props)
                elif model_id == 2:
                    sandpile.set_up(props)
                elif model_id == 3:
                    segregation.set_up(props)
                elif model_id == 4:
                    wolfsheep.set_up(props)
            except TypeError:
                return ('this is for testing')
            return {"Menu": load_menu()}
        except ValueError:
            return err_return("Invalid model answer " + str(model_id))


@api.route("/models/menu/<int:model_id>/")
class ModelMenu(Resource):
    global user

    def get(self, model_id):
        return user()


@api.route("/models/menu/<int:model_id>/<int:menu_id>")
class MenuItem(Resource):
    global user

    def put(self, menu_id):
        if menu_id >= 0 and menu_id < 6 and (type(menu_id) is int):
            return user(menu_id)
        else:
            return err_return("Invalid menu id " + str(menu_id))
        # return {"execute menu item": menuitem_id, "Menu": load_menu()}  # noqa E501


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
