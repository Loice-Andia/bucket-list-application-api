import unittest
from app.test_config import GlobalTestCase

# your test cases


class BucketListItemTest(GlobalTestCase):

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


if __name__ == '__main__':
    unittest.main()
