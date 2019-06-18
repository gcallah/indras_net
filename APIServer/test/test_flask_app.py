from unittest import TestCase, main
from APIServer.flask_app import app, HelloWorld, Models, Props, ModelMenu, MenuItem, err_return, load_models, load_menu
from flask_restplus import Resource, Api, fields
import random
# import json

model_menu = [{"model ID": 0,
               "name": "Adam Smith's Fashion Model",
               "doc": "A model of trendsetters and followers in the world of fashion."
               },
              {"model ID": 1,
               "name": "Forest Fire",
               "doc": "A model forest with trees that randomly catch fire."
               },
              {"model ID": 2,
               "name": "Abelian Sandpile",
               "doc": "A sandpile that makes colorful patterns as the sand tumbles down."
               },
              {"model ID": 3,
               "name": "Schelling's Segregation Model",
               "doc": "Thomas Schelling's famous model of segregated neighborhoods."
               },
              {"model ID": 4,
               "name": "Predator-Prey Model",
               "doc": "Wolves eat sheep in a meadow and their populations' cycle."
               }
              ]

model_cmenu = [{"model ID": 0,
               "name": "Adam Smith's Fashion Model",
               "run": "fashion",
               "props": "models/props/fashion.props.json",
               "doc": "A model of trendsetters and followers in the world of fashion."
               },
              {"model ID": 1,
               "name": "Forest Fire",
               "run": "forestfire",
               "props": "models/props/forestfire.props.json",
               "doc": "A model forest with trees that randomly catch fire."
               },
              {"model ID": 2,
               "name": "Abelian Sandpile",
               "run": "sandpile",
               "props": "models/props/sandpile.props.json",
               "doc": "A sandpile that makes colorful patterns as the sand tumbles down."
               },
              {"model ID": 3,
               "name": "Schelling's Segregation Model",
               "run": "segregation",
               "props": "models/props/segregation.props.json",
               "doc": "Thomas Schelling's famous model of segregated neighborhoods."
               },
              {"model ID": 4,
               "name": "Predator-Prey Model",
               "run": "wolfsheep",
               "props": "models/props/wolfsheep.props.json",
               "doc": "Wolves eat sheep in a meadow and their populations' cycle."
               }
              ]

props_0 = {"grid_height": {"val": 20, "question": "What is the grid height?", "atype": "INT", "hival": 100, "loval": 2},
           "grid_width": {"val": 20, "question": "What is the grid width?", "atype": "INT", "hival": 100, "loval": 2},
           "num_blue": {"val": 20, "question": "How many blue agents do you want?", "atype": "INT", "hival": 100, "loval": 1},
           "num_red": {"val": 20, "question": "How many red agents do you want?", "atype": "INT", "hival": 100, "loval": 1}
           }

props_1 = {"grid_height": {"val": 20, "question": "What is the grid height?", "atype": "INT", "hival": 100, "loval": 2},
           "grid_width": {"val": 20, "question": "What is the grid width?", "atype": "INT", "hival": 100, "loval": 2},
           "density": {"val": 0.44, "question": "What density of trees in the forest would you like?", "atype": "DBL", "hival": 1, "loval": 0}
           }

props_2 = {"grid_height": {"val": 19, "question": "What is the grid height?", "atype": "INT", "hival": 100, "loval": 2},
           "grid_width": {"val": 19, "question": "What is the grid width?", "atype": "INT", "hival": 100, "loval": 2}
           }

props_3 = {"grid_height": {"val": 20, "question": "What is the grid height?", "atype": "INT", "hival": 100, "loval": 2},
           "grid_width": {"val": 20, "question": "What is the grid width?", "atype": "INT", "hival": 100, "loval": 2},
           "num_blue": {"val": 100, "question": "How many blue agents do you want?", "atype": "INT", "hival": 100, "loval": 1},
           "num_red": {"val": 100, "question": "How many red agents do you want?", "atype": "INT", "hival": 100, "loval": 1},
           "mean_tol": {"val": 0.5, "question": "What tolerance should agents have?", "atype": "DBL", "hival": 0.9, "loval": 0.1},
           "tol_deviation": {"val": 0.2, "question": "What should the standard deviation of the agents' tolerance be?", "atype": "DBL", "hival": 0.3, "loval": 0.01}
           }

props_4 = {"grid_height": {"val": 20, "question": "What is the grid height?", "atype": "INT", "hival": 100, "loval": 2},
           "grid_width": {"val": 20, "question": "What is the grid width?", "atype": "INT", "hival": 100, "loval": 2},
           "num_sheep": {"val": 20, "question": "How many sheep do you want?", "atype": "INT", "hival": 100, "loval": 1},
           "num_wolves": {"val": 20, "question": "How many wolves do you want?", "atype": "INT", "hival": 100, "loval": 1}
           }

menu = [{"val": 0, "func": "run", "question": "Run for N periods"},
        {"val": 1, "func": "line_graph", "question": "Display a population graph."},
        {"val": 2, "func": "scatter_plot", "question": "Display a scatter plot."},
        {"val": 3, "func": "ipython", "question": "Leave menu for interactive python session."},
        {"val": 4, "func": "leave", "question": "Quit)."}
        ]


class Test(TestCase):
    def setUp(self):
        self.HelloWorld = HelloWorld(Resource)
        self.Model = Models(Resource)
        self.Props = Props(Resource)
        self.ModelMenu = ModelMenu(Resource)
        self.MenuItem = MenuItem(Resource)
        self.LoadModels = load_models()
        self.LoadMenu = load_menu()

    def test_load_models(self):
        """
        See if models can be loaded.
        """
        rv = self.LoadModels
        self.assertEqual(rv, model_cmenu)

    def test_load_menu(self):
        """
        See if the menu can be loaded.
        """
        rv = self.LoadMenu
        self.assertEqual(rv, menu)

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
        self.assertEqual(rv, model_menu)

    def test_get_props(self):
        """
        See if we can get props.
        """
        model_id = random.randint(0,4)
        rv = self.Props.get(model_id)
        if model_id == 0:
            self.assertEqual(rv, props_0)
        elif model_id == 1:
            self.assertEqual(rv, props_1)
        elif model_id == 2:
            self.assertEqual(rv, props_2)
        elif model_id == 3:
            self.assertEqual(rv, props_3)
        else:
            self.assertEqual(rv, props_4)
        model_id = 5
        rv = self.Props.get(model_id)
        self.assertEqual(rv, {'Error:': 'Invalid model id 5'})
        
    def test_put_props(self):
        """
        Test whether we are able to put props
        """
        model_id = random.randint(0, 4)
        with app.test_request_context():
            rv = self.Props.put(model_id)
        self.assertEqual(rv, {"Menu": menu})

    def test_get_ModelMenu(self):
        """
        Testing whether we are getting the menu.
        """
        model_id = random.randint(0, 4)
        rv = self.ModelMenu.get(model_id)
        self.assertEqual(rv, menu)
        
    def test_put_MenuItem(self):
        """
        Testing whether we are able to put the menu in
        """
        menuitem_id = random.randint(0, 4)
        model_id = random.randint(0,4)
        rv = self.MenuItem.put(model_id, menuitem_id)
        self.assertEqual(rv, {"execute menu item": menuitem_id, "Menu": menu})

    def test_err_return(self):
        """
        Testing whether we are able to get the right error message
        """
        rv = err_return("error message")
        self.assertEqual(rv, {"Error:": "error message"})


if __name__ == "__main__":
    main()