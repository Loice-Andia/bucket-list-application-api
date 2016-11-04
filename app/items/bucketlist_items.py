import json
from app import db
from app.models.bucketlist_models import Bucketlists, Items
from app.bucketlist.bucketlists import decode_token
from datetime import datetime
from flask import jsonify, request
from flask_restful import abort, Resource


class BucketListItems(Resource):
    def get(self, bucketlist_id):
        """ List all bucketlists created by the user"""
        result = {}
        item_list = []
        decode_token(request)
        bucketlist = Bucketlists.query.filter_by(
            bucketlist_id=bucketlist_id).first()
        if bucketlist is None:
            abort(400, message="Wrong bucketlist ID")
        query_string = request.args.to_dict()
        limit = int(query_string.get('limit', 20))
        page_no = int(query_string.get('page', 1))
        if type(limit) is not int:
            abort(400, message="Limit must be an integer")
        if type(page_no) is not int:
            abort(400, message="Limit must be an integer")

        if 'q' in query_string:
            search_result = Items.query.filter(
                Items.name.ilike('%' + query_string['q'] + '%')).paginate(
                page_no, limit)
            if not len(search_result.items):
                abort(
                    400,
                    message="{} does not match any bucketlist item names".format(
                        query_string['q']))
            for item in search_result.items:
                if item.bucketlist_id is int(bucketlist_id):
                    result = {
                        "id": item.item_id,
                        "name": item.name,
                        "description": item.description,
                        "completed": item.completed,
                        "date_created": item.date_created,
                        "date_modified": item.date_modified,
                        "bucketlist": item.bucketlist.name,
                        "owner": item.bucketlist.creator.username}
                item_list.append(result)
            return jsonify(item_list)
        bucketlist_items = Items.query.filter_by(bucketlist_id=bucketlist_id).paginate(
            page_no, limit)
        if not len(bucketlist_items.items):
            abort(400, message="Bucketlist does not have items")
        for item in bucketlist_items.items:
            result = {
                "id": item.item_id,
                "name": item.name,
                "description": item.description,
                "completed": item.completed,
                "date_created": item.date_created,
                "date_modified": item.date_modified,
                "bucketlist": item.bucketlist.name,
                "owner": item.bucketlist.creator.username
            }
            item_list.append(result)
        next_page = 'None'
        previous_page = 'None'
        if bucketlist_items.has_next:
            next_page = '{}api/v1/bucketlists/{}/items?limit={}&page={}'.format(
                str(request.url_root),
                str(bucketlist_id),
                str(limit),
                str(page_no + 1))
        if bucketlist_items.has_prev:
            previous_page = '{}api/v1/bucketlists/{}/items?limit={}&page={}'.format(
                str(request.url_root),
                str(bucketlist_id),
                str(limit),
                str(page_no - 1))
        return jsonify({'bucketlist items': item_list,
                        'total pages': bucketlist_items.pages,
                        'previous': previous_page,
                        'next': next_page})

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
            single_item.date_modified = datetime.utcnow()
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
