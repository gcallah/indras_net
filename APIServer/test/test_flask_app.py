from unittest import TestCase, main
from APIServer.flask_app import app, HelloWorld
from flask_restplus import Resource, Api, fields


class HelloWorldTest(TestCase):
    def setUp(self):
        self.HelloWorld = HelloWorld(Resource)

    def test_HelloWorld(self):
        """
        See if HelloWorld works.
        """
        rv = self.HelloWorld.get()
        self.assertEqual(rv, {'hello': 'world'})

if __name__ == "__main__":
    main()
