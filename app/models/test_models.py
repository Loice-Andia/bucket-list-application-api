import datetime
import unittest
from app import db
from app.test_config import GlobalTestCase
from .bucketlist_models import Bucketlists, Items, Users


class ModelsTest(GlobalTestCase):
    """
    This is the class for testing all the models: Users,
    Bucketlists and Items
    It contains tests for Creation, Editing and Deleting
    of items in the models."""

    def setUp(self):
        db.create_all()
        self.user = Users(
            username="user",
            email="user@gmail.com",
            password="user"
        )
        db.session.add(self.user)
        db.session.commit()
        user = Users.query.filter_by(username='user').first()
        self.bucketlist = Bucketlists(
            name="holiday",
            description="Holiday plans bucketlist",
            date_created=datetime.datetime.utcnow(),
            creator_id=user.user_id
        )
        db.session.add(self.bucketlist)
        db.session.commit()
        bucketlist = Bucketlists.query.filter_by(name='holiday').first()
        self.bucketlist_items = Items(
            name="beach",
            description="Visit diani beach",
            completed=False,
            date_created=datetime.datetime.utcnow(),
            bucketlist_id=bucketlist.bucketlist_id
        )
        db.session.add(self.bucketlist_items)
        db.session.commit()

    def test_can_create_user(self):
        user = Users.query.filter_by(username='user').first()
        self.assertIsInstance(self.user, Users)
        self.assertIsNotNone(user.username)
        self.assertEqual(user.email, 'user@gmail.com')

    def test_can_edit_user(self):
        self.user.email = 'user@yahoo.com'
        db.session.merge(self.user)
        db.session.commit()
        user = Users.query.filter_by(username='user').first()
        self.assertEqual(user.email, 'user@yahoo.com')

    def test_can_create_bucketlist(self):
        bucketlist = Bucketlists.query.filter_by(name='holiday').first()
        self.assertIsInstance(self.bucketlist, Bucketlists)
        self.assertIsNotNone(bucketlist.name)
        self.assertEqual(bucketlist.name, 'holiday')

    def test_can_edit_bucketlist(self):
        self.bucketlist.name = 'Kenyan Holiday'
        db.session.add(self.bucketlist)
        db.session.commit()
        bucketlist = Bucketlists.query.filter_by(name='Kenyan Holiday').first()
        self.assertEqual(bucketlist.name, 'Kenyan Holiday')

    def test_can_create_item_in_a_bucketlist(self):
        item = Items.query.filter_by(name='beach').first()
        self.assertIsInstance(self.bucketlist_items, Items)
        self.assertIsNotNone(item.name)
        self.assertEqual(item.name, 'beach')

    def test_can_edit_item_in_bucketlist(self):
        self.bucketlist_items.name = 'Diani beach'
        db.session.add(self.bucketlist_items)
        db.session.commit()
        item = Items.query.filter_by(name='Diani beach').first()
        self.assertEqual(item.name, 'Diani beach')

    def test_can_delete_item_in_bucketlist(self):
        db.session.delete(self.bucketlist_items)
        db.session.commit()
        item = Items.query.filter_by(name='Diani beach').first()
        self.assertEqual(item, None)

    def tearDown(self):
        db.session.close_all()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
