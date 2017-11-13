import unittest

import main


class TestMain(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMain, self).__init__(*args, **kwargs)

    def test_main(self):
        main.main(subreddit="AdviceAnimals", post_count=10, limit=10)


if __name__ == '__main__':
    unittest.main()
