import datetime
import json
import unittest
from app import db
from app.models.bucketlist_models import Bucketlists, Users
from app.test_config import GlobalTestCase
from flask import url_for


class BucketListItemTest(GlobalTestCase):

    def setUp(self):
        db.create_all()
        self.user = Users(
            username='Loice',
            email='loiceandia@gmail.com',
            password='loice')
        db.session.add(self.user)
        db.session.commit()
        user = Users.query.filter_by(username='Loice').first()
        self.bucketlist = Bucketlists(
            name="test_bucketlist",
            description="Holiday plans bucketlist",
            time_created=str(datetime.datetime.now()),
            creator_id=user.id
        )
        db.session.add(self.bucketlist)
        db.session.commit()
        response = self.client.post(
            url_for('login'),
            data=json.dumps({
                'username': 'Loice',
                'password': 'loice'}),
            content_type="application/json")
        self.token = response.json
        self.test_bucketlist = Bucketlists.query.filter_by(name='test_bucketlist').first()

    def test_bucketlist_endpoint(self):
        response = self.client.get('/bucketlists/1/items/')
        self.assert_200(response)

        response = self.client.post('/bucketlists/1/items/')
        self.assert_200(response)

        response = self.client.put('bucketlists/1/items/1')
        self.assert_200(response)

        response = self.client.delete('bucketlists/1/items/1')
        self.assert_200(response)

        response = self.client.get('/bucketlists/1/items?q=item1')
        self.assert_200(response)

    def test_can_add_items_to_a_bucketlist(self):
        response = self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'bucketlist_id': self.test_bucketlist.id
            }),
            content_type='application/json',
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_view_one_bucketlist_item(self):
        response = self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'bucketlist_id': self.test_bucketlist.id
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('one_item', bucketlist_id=1, item_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_view_items_in_a_bucketlist(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'bucketlist_id': self.test_bucketlist.id
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('items', bucketlist_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_edit_item_in_a_bucketlist(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'bucketlist_id': self.test_bucketlist.id
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.put(
            url_for('one_item', bucketlist_id=1, item_id=1),
            data=json.dumps({
                'name': 'Cook Risotto',
                'description': 'Test_item',
                'completed': False,
                'bucketlist_id': self.test_bucketlist.id
            }),
            content_type='application/json',
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_delete_bucketlist_item(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'bucketlist_id': self.test_bucketlist.id
            }),
            content_type='application/json',
            headers=self.token)

        response = self.client.delete(
            url_for('one_item', bucketlist_id=1, item_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_search_for_item_in_bucketlist(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'bucketlist_id': self.test_bucketlist.id
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('search_items', bucketlist_id=1, query='item'),
            headers=self.token)
        self.assert_200(response)
        result = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(result)

    def tearDown(self):
        db.session.close_all()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
