import pprint
import unittest

from main_redditscrape import RedditScraper

class TestScrape(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestScrape, self).__init__(*args, **kwargs)

    def test_scrape_plz(self):
        r = RedditScraper()
        r.scrape_reddit("AdviceAnimals", pages=1)

if __name__ == '__main__':
    unittest.main()
