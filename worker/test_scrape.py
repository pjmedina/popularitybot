import unittest
import reddit
import random
from worker.reddit import ScrapedRedditPost
import logging


class TestScrape(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestScrape, self).__init__(*args, **kwargs)
        logging.basicConfig(filename="test.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

    def test_scrape(self):
        for scraped_info in reddit.scrape_reddit(subreddit="AdviceAnimals", post_count=1, limit=1):
            self.assertIsNotNone(scraped_info)
            self.assertIsNotNone(scraped_info.posts)
            self.assertIsNotNone(scraped_info.image_urls)
            self.assertIsNotNone(scraped_info.user_info)

    def test_remove_items_from_scrape(self):
        for scraped_info in reddit.scrape_reddit(subreddit="AdviceAnimals", post_count=5, limit=5):
            scraped_info.posts[0] = None
            scraped_info.image_urls[1] = None
            scraped_info.user_info[2] = None
            ScrapedRedditPost.clean(scraped_info)
            self.assertTrue(len(scraped_info.posts) == 2)
            self.assertTrue(len(scraped_info.image_urls) == 2)
            self.assertTrue(len(scraped_info.user_info) == 2)
            rand_int = random.randint(0, len(scraped_info.posts) - 1)
            rand_post_id = scraped_info.posts[rand_int]['data']['id']
            self.assertNotAlmostEqual(rand_post_id, "")


if __name__ == '__main__':
    unittest.main()
