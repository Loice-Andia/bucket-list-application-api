import datetime
import unittest
from app import db
from app.test_config import GlobalTestCase
from app.models.bucketlist_models import Bucketlists, Items, Users


class UserModelTest(GlobalTestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.user = Users(
            id=1,
            username="user",
            email="user@gmail.com",
            password="user"
        )
        db.session.add(self.user)
        db.session.commit()

    def test_can_create_user(self):
        user = Users.query.filter_by(id=1)
        self.assertIsInstance(self.user, Users)
        self.assertIsNotNone(user.username)
        self.assertEqual(user.email, 'user@gmail.com')

    def test_can_edit_user(self):
        self.user.email = 'user@yahoo.com'
        db.session.add(self.user)
        db.session.commit()
        user = Users.query.filter_by(id=1)
        self.assertEqual(user.email, 'user@yahoo.com')

    def test_can_delete_user(self):
        db.session.delete(self.user)
        db.session.commit()
        user = Users.query.filter_by(id=1)
        self.assertRaises(user)


class BucketlistModelTest(GlobalTestCase):

    def setUp(self):
        db.create_all()
        self.bucketlist = Bucketlists(
            id=1,
            name="holiday",
            description="Holiday plans bucketlist",
            time_created=datetime.datetime.utcnow(),
            creator_id=self.user.id
        )
        db.session.add(self.bucketlist)
        db.session.commit()

    def test_can_create_bucketlist(self):
        bucketlist = Bucketlists.query.filter_by(id=1)
        self.assertIsInstance(self.bucketlist, Bucketlists)
        self.assertIsNotNone(bucketlist.name)
        self.assertEqual(bucketlist.name, 'holiday')

    def test_can_edit_bucketlist(self):
        self.bucketlist.name = 'Kenyan Holiday'
        db.session.add(self.bucketlist)
        db.session.commit()
        bucketlist = Bucketlists.query.filter_by(id=1)
        self.assertEqual(bucketlist.name, 'Kenyan Holiday')

    def test_can_delete_bucketlist(self):
        db.session.delete(self.bucketlist)
        db.session.commit()
        bucketlist = Bucketlists.query.filter_by(id=1)
        self.assertRaises(bucketlist)


class ItemsModelTest(GlobalTestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.holiday_items = Items(
            id=1,
            name="beach",
            description="Visit diani beach",
            completed=False,
            bucketlist_id=self.holiday.id
        )
        db.session.add(self.holiday_items)
        db.session.commit()

    def test_can_create_item_in_a_bucketlist(self):
        item = Items.query.filter_by(id=1)
        self.assertIsInstance(self.holiday_items, Items)
        self.assertIsNotNone(item.name)
        self.assertEqual(item.name, 'beach')

    def test_can_edit_item_in_bucketlist(self):
        self.holiday_items.name = 'Diani beach'
        db.session.add(self.holiday_items)
        db.session.commit()
        item = Items.query.filter_by(id=1)
        self.assertEqual(item.name, 'Diani beach')

    def test_can_delete_item_in_bucketlist(self):
        db.session.delete(self.holiday_items)
        db.session.commit()
        item = Items.query.filter_by(id=1)
        self.assertRaises(item)

    def tearDown(self):
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
