from flask import jsonify
from flask_restful import Resource


class Index(Resource):
    def get(self):
        return jsonify({"message": "Welcome to the BucketList API."
                        " Register a new user by sending a"
                        " POST request to /auth/register. "
                        "Login by sending a POST request to"
                        " /auth/login to get started."})


class Login(Resource):
    def get(self):
        pass

    def post(self):
        pass
