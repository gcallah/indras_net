import os
from unittest import TestCase, main
from APIServer.flask_app import app, HelloWorld
from flask_restplus import Resource, Api, fields

# TEST_DB = 'test.db'
# class BasicTests(TestCase):
#     def setUp(self):
#         # app.config['TESTING'] = True
#         # app.config['WTF_CSRF_ENABLED'] = False
#         # app.config['DEBUG'] = False
#         # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#         #                                         os.path.join(app.config['BASEDIR'], TEST_DB)
#         self.app = app.test_client()
#         db.drop_all()
#         db.create_all()
#
#     # executed after each test
#     def tearDown(self):
#         pass
#
#     def test_main_page(self):
#         response = self.app.get('/', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)

class HelloWorldTest(TestCase):
    def setUp(self):
        self.HelloWorld = HelloWorld(Resource)

    def test_HelloWorld(self):
        rv = self.HelloWorld.get()
        self.assertEqual(rv, {'hello': 'world'})

if __name__ == "__main__":
    main()
