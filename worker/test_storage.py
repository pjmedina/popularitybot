import unittest
import reddit
from storage import Storage


class TestStorage(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestStorage, self).__init__(*args, **kwargs)

        # Will throw an exception if storage_creds.ini does not exist,
        # rendering all tests useless. Must have the config file available.
        self.storage = Storage(config_file='storage_creds.ini',
                               config_header='database_info',
                               new_collection_name='test_new_jsons',
                               user_collection_name='test_user_jsons',
                               vision_collection_name='test_vision_info')
        self.client = self.storage.client
        self.db = self.storage.db

    def test_ping(self):
        ping_result = self.db.command('ping')
        self.assertEqual(ping_result['ok'], 1.0)

    def test_testdb(self):
        testdoc = self.db.test
        record = testdoc.find_one()
        self.assertEqual(record['test'], "abc123")

    def test_scrape_storage(self):
        for scraped_info in reddit.scrape_reddit(subreddit="AdviceAnimals", post_count=1, limit=1):
            self.storage.add_reddit_scraped_info(scraped_info)


if __name__ == '__main__':
    unittest.main()
