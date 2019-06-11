# Indra API server
import os
from indra.user import APIUser
from flask import Flask
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

user = APIUser("Dennis", None)

indra_dir = os.getenv("INDRA_HOME", ".")


def load_models():
    try:
        with open(indra_dir + "/models/models.json") as file:
            return json.loads(file.read())["models_database"]
    except FileNotFoundError:
        return {"Error": "File not found"}


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/models')
class Models(Resource):
    def get(self):
        global indra_dir

        models_db = load_models()
        models_response = []
        for model in models_db:
            doc = ""
            if "doc" in model:
                doc = model["doc"]
            models_response.append({"name": model["name"], "doc": doc})
        return models_response


props = api.model("props", {
    "model ID": fields.Integer,
    "props": fields.String("Enter propargs.")
})


@api.route('/models/<int:model_id>/props')
class Props(Resource):
    global indra_dir

    def get(self, model_id):
        try:
            models_db = load_models()
            with open(indra_dir + "/" + models_db[model_id]["props"]) as file:
                props = json.loads(file.read())
                return props
        except (IndexError, KeyError, ValueError):
            return {"Error": "Invalid model id " + str(model_id)}
        except FileNotFoundError:
            return {"Error": "File not found"}

    @api.expect(props)
    def put(self, model_id):
        try:
            # update props
            props = api.payload  # noqa F841
            return {"Menu": "menu will be returned here"}
        except ValueError:
            return {"Error": "Invalid model answer " + str(model_id)}


@api.route("/models/<int:model_id>/menu")
class Menu(Resource):
    global user

    def get(self, model_id):
        return user()

    def put(self, menuitem_id):
        return {"execute menu item": menuitem_id, "Menu": "menu will be returned here"}  # noqa E501


# Ask Professor!!!!!
# @api.route('/models//menu')
# class Model(Resource):
#     def put(self, model_id):
#         return {"name": models_db[model_id]["name"],
#                 "status": "Is running!",
#                 "menu": ["Item 1", "Item 2", "Item 3"]
#                }

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
