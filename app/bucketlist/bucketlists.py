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
                    "time_created": bucketlist.time_created,
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

        if not name:
            abort(400, message="Name cannot be empty")

        bucketlist = Bucketlists.query.filter_by(
            name=name,
            creator_id=user_id).first()
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
        result = {}
        user_id = decode_token(request)
        single_bucketlist = Bucketlists.query.filter_by(
            creator_id=user_id,
            id=bucketlist_id).first()
        if not single_bucketlist:
            abort(400, message="No bucketlist matching the id {}".format(
                bucketlist_id))
        result.update({
            single_bucketlist.id: {
                "name": single_bucketlist.name,
                "description": single_bucketlist.description,
                "creator": single_bucketlist.creator.username
            }})
        return jsonify(result)

    def put(self, bucketlist_id):
        user_id = decode_token(request)
        if bucketlist_id is None:
            abort(400, message="Missing bucketlist ID")
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(
                400,
                message="No params passed.Kindly fill the name and description.")

        single_bucketlist = Bucketlists.query.filter_by(
            creator_id=user_id,
            id=bucketlist_id).first()
        print (single_bucketlist)
        if not single_bucketlist:
            abort(400, message="No bucketlist matching the id {}".format(
                bucketlist_id))

        try:
            if 'name' in data.keys():
                single_bucketlist.name = data['name']
            if 'description' in data.keys():
                single_bucketlist.description = data['description']
            db.session.add(single_bucketlist)
            db.session.commit()
            return jsonify({
                'message': "{} bucketlist updated successfully".format(single_bucketlist.name)})
        except Exception:
            abort(500, message="Bucketlist not updated")

    def delete(self, bucketlist_id):
        user_id = decode_token(request)
        if bucketlist_id is None:
            abort(400, message="Missing bucketlist ID")
        single_bucketlist = Bucketlists.query.filter_by(
            creator_id=user_id,
            id=bucketlist_id).first()
        if not single_bucketlist:
            abort(400, message="No bucketlist matching the id {}".format(
                bucketlist_id))
        try:
            db.session.delete(single_bucketlist)
            db.session.commit()
            return jsonify({
                'message': "{} bucketlist deleted successfully".format(
                    single_bucketlist.name)})
        except Exception:
            abort(500, message="Bucketlist not deleted")


class SearchBucketlist(Resource):
    def post(self, query):
        user_id = decode_token(request)
        import ipdb
        ipdb.set_trace()
        search_result = Bucketlists.query.filter_by(
            Bucketlists.name.like('%' + query + '%'),
            creator_id=user_id).all()
        if not len(search_result):
            abort(400, message="{} does not match any bucktlist names".format(
                query))
        for bucketlist in search_result:
            result.update({
                bucketlist.id: {
                    "name": bucketlist.name,
                    "description": bucketlist.description,
                    "time_created": bucketlist.time_created,
                    "creator": bucketlist.creator.username
                }})
        return jsonify(result)
