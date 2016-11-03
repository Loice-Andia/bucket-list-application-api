import json
import unittest
from app import db
from app.models.bucketlist_models import Users
from app.test_config import GlobalTestCase
from flask import url_for


class RegistrationTest(GlobalTestCase):

    def setUp(self):
        db.create_all()

    def test_register_endpoint(self):
        response = self.client.get(url_for('register'))
        data = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 200)
        self.assertEqual('To register,send a POST request with username, password and email to /auth/register.',
                         data['message'])

    def test_registration_of_a_new_user(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps(
                {'username': 'Loice',
                 'password': 'loice',
                 'email': 'loice@gmail.com'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("created successfully",
                      data['message'])

    def test_registration_of_existing_user(self):
        user = Users(
            username='Loice',
            email='loiceandia@gmail.com',
            password='loice')
        db.session.add(user)
        db.session.commit()
        response = self.client.post(
            url_for('register'),
            data=json.dumps(
                {'username': 'Loice',
                 'email': 'loice@gmail.com',
                 'password': 'loice'}),
            content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("User already exists",
                      data['message'])

    def test_registration_with_short_password(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps({
                'username': 'Trial',
                'email': 'trial@gmail.com',
                'password': '123'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("Password should be 4 or more characters",
                      data['message'])

    def test_incomplete_details_on_registration(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps({'username': 'Loice'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("provide a username, email and password",
                      data['message'])

    def tearDown(self):
        db.session.close_all()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
