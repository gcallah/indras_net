"""
"""
from unittest import TestCase, main, skip
import json
import random
from flask_restplus import Resource, Api, fields

from APIServer.api_endpoints import app, HelloWorld, Models
from APIServer.api_endpoints import Props, ModelMenu, Run
from APIServer.api_endpoints import load_menu
from APIServer.api_endpoints import indra_dir
from APIServer.models_api import load_models
from APIServer.api_utils import err_return

menu = [{"val": 0, "func": "run", "question": "Run for N periods"},
        {"val": 1, "func": "line_graph", "question": "Display a population graph."},
        {"val": 2, "func": "scatter_plot", "question": "Display a scatter plot."},
        {"val": 3, "func": "ipython", "question":
         "Leave menu for interactive python session."},
        {"val": 4, "func": "leave", "question": "Quit)."}
        ]


class Test(TestCase):
    def setUp(self):
        # none of the object's members names should have caps!
        self.HelloWorld = HelloWorld(Resource)
        self.Model = Models(Resource)
        self.Props = Props(Resource)
        self.ModelMenu = ModelMenu(Resource)
        self.Run = Run(Resource)
        self.LoadModels = load_models(indra_dir)
        self.LoadMenu = load_menu()

    def test_load_models(self):
        """
        See if models can be loaded.
        """
        rv = self.LoadModels
        test_model_file = indra_dir + "/models/models.json"
        with open(test_model_file) as file:
            test_rv = json.loads(file.read())["models_database"]
        self.assertEqual(rv, test_rv)

    def test_load_menu(self):
        """
        See if the menu can be loaded.
        """
        rv = self.LoadMenu
        test_menu_file = indra_dir + "/indra/menu.json"
        with open(test_menu_file) as file:
            test_rv = json.loads(file.read())["menu_database"]
        self.assertEqual(rv, test_rv)

    def test_hello_world(self):
        """
        See if HelloWorld works.
        """
        rv = self.HelloWorld.get()
        self.assertEqual(rv, {'hello': 'world'})

    def test_get_model(self):
        """
        See if we can get models.
        """
        rv = self.Model.get()

        test_model_file = indra_dir + "/models/models.json"
        with open(test_model_file) as file:
            test_models_db = json.loads(file.read())["models_database"]

        test_models_response = []
        for model in test_models_db:
            doc = ""
            if "doc" in model:
                doc = model["doc"]
            test_models_response.append({"model ID": model["model ID"],
                                    "name": model["name"],
                                    "doc": doc,
                                    "source": model["source"]})

        self.assertEqual(rv, test_models_response)

    @skip("Skipping get props.")
    def test_get_props(self):
        """
        See if we can get props.
        """
        model_id = random.randint(0, 10)
        rv = self.Props.get(model_id)

        test_model_file = indra_dir + "/models/models.json"
        with open(test_model_file) as file:
            test_models_db = json.loads(file.read())["models_database"]

        with open(indra_dir + "/" + test_models_db[model_id]["props"]) as file:
            test_props = json.loads(file.read())

        self.assertEqual(rv, test_props)

    @skip("Skipping put props while json format is in flux.")
    def test_put_props(self):
        """
        Test whether we are able to put props
        """
        model_id = random.randint(0, 10)
        with app.test_request_context():
            rv = self.Props.put(model_id)
        self.assertEqual(type(rv), dict)

    def test_get_ModelMenu(self):
        """
        Testing whether we are getting the menu.
        """
        rv = self.ModelMenu.get()
        test_menu_file = indra_dir + "/indra/menu.json"
        with open(test_menu_file) as file:
            test_menu = json.loads(file.read())["menu_database"]
        self.assertEqual(rv, test_menu)

    def test_err_return(self):
        """
        Testing whether we are able to get the right error message
        """
        rv = err_return("error message")
        self.assertEqual(rv, {"Error:": "error message"})


if __name__ == "__main__":
    main()
