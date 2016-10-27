import json
import unittest
from app import db
from app.models.bucketlist_models import Users
from app.test_config import GlobalTestCase
from flask import url_for


class RegistrationTest(GlobalTestCase):

    def test_register_endpoint(self):
        response = self.client.get('/auth/register')
        self.assert_200(response)

    def test_registration_of_a_new_user(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps(
                {'username': 'Loice',
                 'password': 'loice',
                 'email': 'loice@gmail.com'}),
            content_type='application/json')
        self.assertIn('Loice', response.data)
        self.assertEqual(response.status_code, 201)

    def test_registration_of_existing_user(self):
        db.create_all()
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
                 'email': 'loiceandia@gmail.com',
                 'password': 'loice'}),
            content_type='appliction/json')
        self.assertIn('User already exists', response.data)

    def test_registration_with_short_password(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps(
                {'username': 'Trial',
                 'password': '123'}))
        self.assertIn('Password needs to be more than 4 characters',
                      response.data)
        self.assertEquals(response.status_code, 400)

    def test_incomplete_details_on_registration(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps({'username': 'Loice'}),
            content_type='application/json')
        self.assertIn("Bad Request", response.data)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
