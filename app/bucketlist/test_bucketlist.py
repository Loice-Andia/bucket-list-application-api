import unittest
from app.test_config import GlobalTestCase

# your test cases


class BucketlistTest(GlobalTestCase):

    def test_bucketlist_endpoint(self):
        response = self.client.get('/bucketlists/')
        self.assert_200(response)

        response = self.client.post('/bucketlists/')
        self.assert_200(response)

        response = self.client.get('/bucketlists/1')
        self.assert_200(response)

        response = self.client.put('/bucketlists/1')
        self.assert_200(response)

        response = self.client.delete('/bucketlists/1')
        self.assert_200(response)

        response = self.client.get('/bucketlists?q=bucket1')
        self.assert_200(response)


if __name__ == '__main__':
    unittest.main()
