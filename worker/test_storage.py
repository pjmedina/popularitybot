import pprint
import unittest
from storage import Storage


class TestStorage(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestStorage, self).__init__(*args, **kwargs)

        # Will throw an exception if storage_creds.ini does not exist,
        # rendering all tests useless. Must have the config file available.
        self.storage = Storage('storage_creds.ini', 'database_info')
        self.client = self.storage.client
        self.db = self.storage.db

    def test_ping(self):
        ping_result = self.db.command('ping')
        self.assertEqual(ping_result['ok'], 1.0)

    def test_testdb(self):
        testdoc = self.db.test
        record = testdoc.find_one()
        self.assertEqual(record['test'], "abc123")


if __name__ == '__main__':
    unittest.main()
