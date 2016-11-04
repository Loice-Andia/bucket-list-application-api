import datetime
import json
import unittest
from app import db
from app.models.bucketlist_models import Bucketlists, Users, Items
from app.test_config import GlobalTestCase
from flask import url_for


class BucketListItemTest(GlobalTestCase):

    def setUp(self):
        db.drop_all()
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
            date_created=str(datetime.datetime.now()),
            creator_id=user.user_id
        )
        db.session.add(self.bucketlist)
        db.session.commit()
        response = self.client.post(
            url_for('login'),
            data=json.dumps({
                'username': 'Loice',
                'password': 'loice'}),
            content_type="application/json")
        data = json.loads(response.get_data(as_text=True))
        self.token = {'Authorization': data['token']}
        self.test_bucketlist = Bucketlists.query.filter_by(
            name='test_bucketlist').first()

    def test_can_add_items_to_a_bucketlist(self):
        response = self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'date_created': str(datetime.datetime.utcnow()),
                'bucketlist_id': self.test_bucketlist.bucketlist_id
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
                'date_created': str(datetime.datetime.utcnow()),
                'bucketlist_id': self.test_bucketlist.bucketlist_id
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
                'date_created': str(datetime.datetime.utcnow()),
                'bucketlist_id': self.test_bucketlist.bucketlist_id
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
                'date_created': str(datetime.datetime.utcnow()),
                'bucketlist_id': self.test_bucketlist.bucketlist_id
            }),
            content_type='application/json',
            headers=self.token)
        item = Items.query.filter_by(name='item1').first()
        response = self.client.put(
            url_for('one_item', bucketlist_id=1, item_id=item.item_id),
            data=json.dumps({
                'name': 'Cook Risotto',
                'description': 'Test_item',
                'completed': False,
                'bucketlist_id': self.test_bucketlist.bucketlist_id
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
                'date_created': str(datetime.datetime.utcnow()),
                'bucketlist_id': self.test_bucketlist.bucketlist_id
            }),
            content_type='application/json',
            headers=self.token)

        response = self.client.delete(
            url_for('one_item', bucketlist_id=1, item_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

        response = self.client.get(
            url_for('one_item', bucketlist_id=1, item_id=1),
            headers=self.token)
        self.assert_status(response, 400)

    def test_can_search_for_item_in_bucketlist(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'date_created': str(datetime.datetime.utcnow()),
                'bucketlist_id': self.test_bucketlist.bucketlist_id
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            '/api/v1/bucketlists/1/items?q=item',
            headers=self.token)
        self.assert_200(response)
        result = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(result)
        response = self.client.get(
            '/api/v1/bucketlists/1/items?q=none',
            headers=self.token)
        self.assert_status(response, 400)
        result = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(result)
        self.assertIn('does not match any bucketlist item names',
                      result['message'])

    def tearDown(self):
        db.session.close_all()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
