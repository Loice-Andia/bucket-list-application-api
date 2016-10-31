from flask_testing import TestCase
from run import app


class GlobalTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "mysql://root@localhost/bucketlist_test"
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app
