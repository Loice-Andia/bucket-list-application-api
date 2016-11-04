from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(config_name):
    """
    This function creates a Flask instance for
    the application and configures it.
    """
    application = Flask(__name__)

    application.config.from_object(config[config_name])

    db.init_app(application)

    return application


app = create_app('development')
