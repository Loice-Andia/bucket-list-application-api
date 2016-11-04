from flask_testing import TestCase
from run import app


class GlobalTestCase(TestCase):
    """
    This is the global test case class that creates the testing app
    that is used in all test within the application
    """
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "mysql://root@localhost/bucketlist_test"
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app
