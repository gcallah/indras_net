
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask_restplus import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

with open("models/models.json") as file:
    models_database = json.loads(file.read())


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/models')
class Models(Resource):
    def get(self):
        return models_database


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
