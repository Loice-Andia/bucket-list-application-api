from flask_restful import Resource


class BucketListItems(Resource):
    def get(self, bucketlist_id):
        pass

    def post(self, bucketlist_id):
        pass


class OneBucketListItem(Resource):
    def get(self, bucketlist_id, item_id):
        pass

    def post(self, bucketlist_id, item_id):
        pass

    def put(self, bucketlist_id, item_id):
        pass

    def delete(self, bucketlist_id, item_id):
        pass


class SearchBucketlistItems(Resource):
    def get(self, bucketlist_id, query):
        pass

    def post(self, bucketlist_id, query):
        pass
