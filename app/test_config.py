from flask import Flask
from flask_testing import TestCase
from app import db


class GlobalTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "mysql://root:root@localhost/bucketlist_test"
        app.config['TESTING'] = True
        db.init_app(app)
        return app
