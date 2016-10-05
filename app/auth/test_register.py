import unittest
from app.test_config import GlobalTestCase

# your test cases


class RegistrationTest(GlobalTestCase):

    def test_register_endpoint(self):
        response = self.client.get('/auth/register')
        self.assert_200(response)


if __name__ == '__main__':
    unittest.main()
