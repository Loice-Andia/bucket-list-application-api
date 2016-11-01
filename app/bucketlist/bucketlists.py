import json
import jwt
from app import db
from app.models.bucketlist_models import Bucketlists
from config import Config
from datetime import datetime
from flask import jsonify, request
from flask_restful import abort, Resource


def decode_token(request):
    token = request.headers.get('Authorization')
    if not token:
        abort(401, message="No Authorization token")
    try:
        payload = jwt.decode(token, Config.SECRET_KEY)
    except jwt.DecodeError:
        abort(401, message='Token is invalid')
    except jwt.ExpiredSignature:
        abort(401, message="Token has expired.Login to generate another token")

    return payload['sub']


class Bucketlist(Resource):
    def get(self):
        """ List all bucketlists created by the user"""
        result = {}
        user_id = decode_token(request)
        bucketlists = Bucketlists.query.filter_by(creator_id=user_id).all()
        if not len(bucketlists):
            abort(400, message="User does not have bucketlists")
        for bucketlist in bucketlists:
            result.update({
                bucketlist.id: {
                    "name": bucketlist.name,
                    "description": bucketlist.description,
                    "creator": bucketlist.creator.username
                }})
        return jsonify(result)

    def post(self):
        user_id = decode_token(request)
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(
                400,
                message="No params passed.Kindly fill the name and description.")
        name = data['name']
        description = data['description']
        creator_id = user_id

        bucketlist = Bucketlists.query.filter_by(
            name=name, creator_id=user_id).first()
        if bucketlist:
            abort(400, message="{} bucketlist already exists".format(
                bucketlist.name))
        try:
            new_bucketlist = Bucketlists(
                name=name,
                description=description,
                time_created=datetime.utcnow(),
                creator_id=creator_id
            )
            db.session.add(new_bucketlist)
            db.session.commit()
            return jsonify({
                'message': "{} bucketlist created successfully".format(name)})
        except Exception:
            abort(500, message="Bucketlist not created")


class OneBucketlist(Resource):
    def get(self, bucketlist_id):
        pass

    def post(self, bucketlist_id):
        pass

    def put(self, bucketlist_id):
        pass

    def delete(self, bucketlist_id):
        pass


class SearchBucketlist(Resource):
    def get(self, query):
        pass

    def post(self, query):
        pass
