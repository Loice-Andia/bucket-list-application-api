from flask_testing import TestCase
from run import app
from sqlalchemy import create_engine


class GlobalTestCase(TestCase):
    def create_app(self):
        create_engine('mysql://root:root@localhost/bucketlist_test')
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "mysql://root:root@localhost/bucketlist_test"
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app
