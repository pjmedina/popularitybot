import unittest

from worker import main_redditscrape


class TestScrape(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestScrape, self).__init__(*args, **kwargs)

    def test_scrape_task(self):
        for scraped_info in main_redditscrape.scrape_reddit(subreddit="AdviceAnimals", pages=1):
            self.assertIsNotNone(scraped_info)
            self.assertIsNotNone(scraped_info.post)
            self.assertIsNotNone(scraped_info.image_urls)
            self.assertIsNotNone(scraped_info.users)


if __name__ == '__main__':
    unittest.main()
