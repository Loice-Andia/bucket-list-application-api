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
        self.bucketlist = Bucketlists(
            name="test_bucketlist",
            description="Holiday plans bucketlist",
            time_created=datetime.datetime.now(),
        )
        self.bucketlist.creator.add(self.user)
        db.session.add_all(self.user, self.bucketlist)
        db.session.commit()
        response = self.client.post(
            url_for('login'),
            data=json.dumps({
                'username': 'Loice',
                'password': 'loice'}),
            content_type="application/json")
        self.token = response.json

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
                'bucketlist': self.bucketlist
            }),
            content_type='application/json',
            headers=self.token)
        self.assert_200(response)
        self.assertIn("ITEM1 sucessfully added", response.data)

    def test_can_view_items_in_a_bucketlist(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'bucketlist': self.bucketlist
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('items', bucketlist_id=1),
            headers=self.token)
        self.assert_200(response)
        bucketlist_items = json.loads(response.data)
        self.assertEqual(bucketlist_items.get("name"), "item1")

    def test_can_edit_item_in_a_bucketlist(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'bucketlist': self.bucketlist
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.put(
            url_for('items', bucketlist_id=1, item_id=1),
            data=json.dumps({
                'name': 'Cook Risotto',
                'description': 'Test_item',
                'completed': False,
                'bucketlist': self.bucketlist
            }),
            content_type='application/json',
            headers=self.token)
        self.assert_200(response)
        self.assertIn('successfully updated', response.data)

    def test_can_delete_bucketlist_item(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'bucketlist': self.bucketlist
            }),
            content_type='application/json',
            headers=self.token)

        response = self.client.delete(
            url_for('items', bucketlist_id=1, item_id=1),
            headers=self.token)
        self.assert_200(response)
        self.assertIn('successfully deleted', response.data)

    def test_can_search_for_item_in_bucketlist(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'description': 'Test_item',
                'completed': False,
                'bucketlist': self.bucketlist
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('items', bucketlist_id=1, q='item'),
            headers=self.token)
        self.assert_200(response)
        result = json.loads(response.data)
        self.assertEqual(result.get("name"), "item1")

    def tearDown(self):
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
