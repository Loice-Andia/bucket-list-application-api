import json
import unittest
from app import db
from app.models.bucketlist_models import Users
from app.test_config import GlobalTestCase
from flask import url_for


class LoginTest(GlobalTestCase):
    def setUp(self):
        db.create_all()
        user = Users(
            username='Loice',
            email='loiceandia@gmail.com',
            password='loice')
        db.session.add(user)
        db.session.commit()

    def test_index_endpoint(self):
        response = self.client.get('/')
        self.assert_status(response, 302)

    def test_login_endpoint(self):
        response = self.client.get('api/v1/auth/login')
        self.assert_200(response)

    def test_login_with_right_credentials(self):
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {'username': 'Loice',
                 'password': 'loice'}),
            content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_login_with_non_existing_user(self):
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {'username': 'Jimmy',
                 'password': 'jimmy'}),
            content_type='application/json')
        self.assert_status(response, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_login_with_empty_username_or_password(self):
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {'username': '',
                 'password': ''}),
            content_type='application/json')
        self.assert_status(response, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def tearDown(self):
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
