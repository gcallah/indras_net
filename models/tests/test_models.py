from unittest import TestCase, main
from pydoc import locate

import json

models_lst = []

class TestAllModels(TestCase):

    def setUp(self):
        with open ("models.json") as json_file:
            data = json.load(json_file)
            for l in data["models_database"]:
                if l["run"] != "fashion" and l["run"] != "segregation" and l["run"] != "wolfsheep":
                    model = locate("models." + l["run"])
                    env_tup = model.set_up()
                    models_lst.append(env_tup)

    def tearDown(self):
        for i in models_lst:
            for j in i:
                j = None

    def test_models(self):
        for i in models_lst:
            self.assertEqual(i[0].runN() > 0, True)
