import json
from app import db
from app.models.bucketlist_models import Items
from app.bucketlist.bucketlists import decode_token
from flask import jsonify, request
from flask_restful import abort, Resource


class BucketListItems(Resource):
    def get(self, bucketlist_id):
        """ List all bucketlists created by the user"""
        result = {}
        decode_token(request)
        items = Items.query.filter_by(bucketlist_id=bucketlist_id).all()
        if not len(items):
            abort(400, message="Bucketlist does not have items")
        for item in items:
            result.update({
                item.item_id: {
                    "name": item.name,
                    "description": item.description,
                    "completed": item.completed,
                    "bucketlist": item.bucketlist.name,
                    "owner": item.bucketlist.creator.username
                }})
        return jsonify(result)

    def post(self, bucketlist_id):
        decode_token(request)
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(
                400,
                message="No params passed.Kindly fill the name and description.")
        if not data['name']:
            abort(400, message="Name cannot be empty")
        name = data['name']
        description = data['description']
        completed = False
        if 'completed' in data.keys():
            completed = data['completed']

        item = Items.query.filter_by(
            name=name,
            bucketlist_id=bucketlist_id).first()
        if item:
            abort(400, message="{} bucketlist item already exists".format(
                item.name))
        try:
            new_bucketlist_item = Items(
                name=name,
                description=description,
                completed=completed,
                bucketlist_id=bucketlist_id
            )
            db.session.add(new_bucketlist_item)
            db.session.commit()
            return jsonify({
                'message': "{} bucketlist item created successfully".format(
                    name)})
        except Exception:
            abort(500, message="Bucketlist Item not created")


class OneBucketListItem(Resource):
    def get(self, bucketlist_id, item_id):
        result = {}
        decode_token(request)
        if bucketlist_id is None:
            abort(400, message="Missing bucketlist ID")
        if item_id is None:
            abort(400, message="Missing item ID")
        single_item = Items.query.filter_by(
            bucketlist_id=bucketlist_id,
            item_id=item_id).first()
        if not single_item:
            abort(400, message="No item matching the id {} in the bucketlist".format(
                item_id))
        result.update({
            single_item.item_id: {
                "name": single_item.name,
                "description": single_item.description,
                "completed": single_item.completed,
                "bucketlist": single_item.bucketlist.name
            }})
        return jsonify(result)

    def put(self, bucketlist_id, item_id):
        decode_token(request)
        if bucketlist_id is None:
            abort(400, message="Missing bucketlist ID")
        if item_id is None:
            abort(400, message="Missing item ID")
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(
                400,
                message="No params passed.Kindly fill the name and description.")

        single_item = Items.query.filter_by(
            bucketlist_id=bucketlist_id,
            item_id=item_id).first()

        if not single_item:
            abort(400, message="No bucketlist matching the id {}".format(
                bucketlist_id))

        try:
            if 'name' in data.keys():
                single_item.name = data['name']
            if 'description' in data.keys():
                single_item.description = data['description']
            if 'completed' in data.keys():
                single_item.completed = data['completed']
            db.session.add(single_item)
            db.session.commit()
            return jsonify({
                'message': "{} item updated successfully".format(
                    single_item.name)})
        except Exception:
            abort(500, message="Item not updated")

    def delete(self, bucketlist_id, item_id):
        decode_token(request)
        if bucketlist_id is None:
            abort(400, message="Missing bucketlist ID")
        if item_id is None:
            abort(400, message="Missing item ID")
        single_item = Items.query.filter_by(
            bucketlist_id=bucketlist_id,
            item_id=item_id).first()
        if not single_item:
            abort(400, message="No item matching the id {}".format(
                item_id))
        try:
            db.session.delete(single_item)
            db.session.commit()
            return jsonify({
                'message': "{} item deleted successfully".format(
                    single_item.name)})
        except Exception:
            abort(500, message="Item not deleted")


class SearchBucketlistItems(Resource):
    def get(self, bucketlist_id, search_query):
        result = {}
        decode_token(request)
        if search_query:
            search_result = Items.query.filter(
                Items.name.ilike('%' + search_query + '%')).all()

            if not len(search_result):
                abort(
                    400,
                    message="{} does not match any bucketlist item names".format(
                        search_query))
            for item in search_result:
                if item.bucketlist_id is bucketlist_id:
                    result.update({
                        item.item_id: {
                            "name": item.name,
                            "description": item.description,
                            "completed": item.completed}})
            return jsonify(result)
        abort(400, message="Missing search parameter")
