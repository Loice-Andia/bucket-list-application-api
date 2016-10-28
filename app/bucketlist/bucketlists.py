from flask_restful import Resource


class Bucketlist(Resource):
    def get(self):
        pass

    def post(self):
        pass


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
