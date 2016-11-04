import json
from app import db
from flask import jsonify, request
from flask_restful import abort, Resource
from app.models.bucketlist_models import Users


class Register(Resource):
    """
    This is the class for the registration resources.
    GET: Provides the registration instructions.
    POST: Adds a user o the database.
    """
    def get(self):
        return jsonify({"message": "To register,"
                        "send a POST request with username, password and email"
                        " to /auth/register."})

    def post(self):
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(400,
                  message="No params passed. Kindly fill you username, email and password")
        if len(data.keys()) < 3:
            abort(400,
                  message="Ensure you provide a username, email and password")
        if not data['username'] or not data['email'] or not data['password']:
            abort(400,
                  message="Kindly fill in the missing details")

        username = data['username']
        email = data['email']
        password = data['password']

        if len(password) < 4:
            abort(400,
                  message="Password should be 4 or more characters")

        user = Users.query.filter_by(username=username).first()
        if user is not None:
            abort(400, message="User already exists")

        try:
            new_user = Users(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
                'message': "{} created successfully".format(username)})
        except Exception as e:
            abort(500, message="User not created")
