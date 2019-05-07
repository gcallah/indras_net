
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/models')
class Models(Resource):
    models = {
        "Adam Smith's Fashion Model": "models.fashion.main",
        "Forest Fire": "models.forestfire.main",
        "Abelian Sandpile": "models.sandpile.main",
        "Schelling's Segregation Model": "models.segregation.main",
        "Predator-Prey Model": "models.wolfsheep.main"
    }

    def get(self):
        return Models.models


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
