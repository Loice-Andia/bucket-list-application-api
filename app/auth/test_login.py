import unittest
from app.test_config import GlobalTestCase

# your test cases


class LoginTest(GlobalTestCase):
    def test_index_endpoint(self):
        response = self.client.get('/')
        self.assert_200(response)

    def test_login_endpoint(self):
        response = self.client.get('/auth/login')
        self.assert_200(response)


if __name__ == '__main__':
    unittest.main()
