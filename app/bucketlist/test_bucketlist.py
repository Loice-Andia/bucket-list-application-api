import datetime
import json
import unittest
from app import db
from app.models.bucketlist_models import Users
from app.test_config import GlobalTestCase
from flask import url_for


class BucketlistTest(GlobalTestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.user = Users(
            username='Loice',
            email='loiceandia@gmail.com',
            password='loice')
        db.session.add(self.user)
        db.session.commit()
        response = self.client.post(
            url_for('login'),
            data=json.dumps({
                'username': 'Loice',
                'password': 'loice'}),
            content_type="application/json")
        self.token = response.json
        self.logged_in_user = Users.query.filter_by(username='Loice').first()

    def test_bucketlist_endpoint(self):
        response = self.client.get('/bucketlists/')
        self.assert_200(response)

        response = self.client.post('/bucketlists/')
        self.assert_200(response)

        response = self.client.get('/bucketlists/1')
        self.assert_200(response)

        response = self.client.put('/bucketlists/1')
        self.assert_200(response)

        response = self.client.delete('/bucketlists/1')
        self.assert_200(response)

        response = self.client.get('/bucketlists?q=bucket1')
        self.assert_200(response)

    def test_can_create_bucketlist(self):
        response = self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'description': 'Test bucketlist',
                'time_created': str(datetime.datetime.now()),
                'creator_id': self.logged_in_user.id
            }),
            content_type='application/json',
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_view_all_bucketlists(self):
        self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'description': 'Test bucketlist',
                'time_created': str(datetime.datetime.now()),
                'creator_id': self.logged_in_user.id
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('bucketlists', bucketlist_id=None),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_view_one_bucketlist(self):
        self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'description': 'Test bucketlist',
                'time_created': str(datetime.datetime.now()),
                'creator_id': self.logged_in_user.id
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('one_bucketlist', bucketlist_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_delete_bucketlist(self):
        self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'description': 'Test bucketlist',
                'time_created': str(datetime.datetime.now()),
                'creator_id': self.logged_in_user.id
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.delete(
            url_for('one_bucketlist', bucketlist_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_search_for_bucketlist(self):
        self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'description': 'Test bucketlist',
                'time_created': str(datetime.datetime.now()),
                'creator_id': self.logged_in_user.id
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('search_bucketlists', query='test'),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_edit_bucketlist(self):
        self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'description': 'Test bucketlist',
                'time_created': str(datetime.datetime.now()),
                'creator_id': self.logged_in_user.id
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.put(
            url_for('one_bucketlist', bucketlist_id=1),
            data=json.dumps({
                'name': 'Travel',
                'description': 'Test bucketlist',
                'time_created': str(datetime.datetime.now()),
                'creator_id': self.logged_in_user.id
            }),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def tearDown(self):
        db.session.close_all()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
