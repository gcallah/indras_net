# Indra API server
import os
from indra.user import APIUser
from flask import Flask
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
import json
# from models.run_dict import setup_dict
from models.run_dict import rdict


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
        # try:
        ret = api.payload
        # return {str(model_id): type(ret) == dict}
        try:
            # setup_dict[model_id["run"]](ret)
            return str({"Menu": load_menu()}) + "Props:" + str(ret)
        except TypeError:
            return 'not setting up the model'
        # except ValueError:
        #     return err_return("Invalid model answer " + str(model_id))


@api.route("/models/menu/<int:model_id>/")
class ModelMenu(Resource):
    global user

    def get(self, model_id):
        return user()


# @api.route("/models/menu/<int:menu_id>")
@api.route("/models/menu/<int:model_id>/<int:menu_id>")
class MenuItem(Resource):
    global user

    def put(self, model_id, menu_id):
        if 0 <= menu_id < 6 and (type(menu_id) is int):
            try:
                user.tell("execute menu item" + str(menu_id))
                user.tell(str(load_menu()))
                rdict[model_id["run"]](menu_id)
                return user.to_json()
            except TypeError:
                return 'not running the model'
        else:
            return err_return("Invalid menu id " + str(menu_id))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
