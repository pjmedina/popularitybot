import unittest
import reddit
from vision import VisionApi
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
        self.vision = VisionApi()
        self.client = self.storage.client
        self.db = self.storage.db

    def test_ping(self):
        ping_result = self.db.command('ping')
        self.assertEqual(ping_result['ok'], 1.0)

    def test_testdb(self):
        testdoc = self.db.test
        record = testdoc.find_one()
        self.assertEqual(record['test'], "abc123")

    def test_user_exists(self):
        self.assertTrue(self.storage.reddit_user_exists("terpin"))

    def test_scrape_storage(self):
        for scraped_info in reddit.scrape_reddit(subreddit="AdviceAnimals", post_count=1, limit=1):
            self.storage.add_reddit_scraped_info(scraped_info)

            vision_res = self.vision.detect_images_info(scraped_info.image_urls)
            for post, image_url, image_info in zip(scraped_info.posts, scraped_info.image_urls, vision_res['responses']):
                self.storage.add_vision_info(reddit.get_post_id(post), image_url=image_url, vision_json=image_info)


if __name__ == '__main__':
    unittest.main()
