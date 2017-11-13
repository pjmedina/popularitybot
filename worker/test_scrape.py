import unittest

import reddit


class TestScrape(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestScrape, self).__init__(*args, **kwargs)

    def test_scrape(self):
        for scraped_info in reddit.scrape_reddit(subreddit="AdviceAnimals", post_count=1, limit=1):
            self.assertIsNotNone(scraped_info)
            self.assertIsNotNone(scraped_info.posts)
            self.assertIsNotNone(scraped_info.image_urls)
            self.assertIsNotNone(scraped_info.user_info)


if __name__ == '__main__':
    unittest.main()
