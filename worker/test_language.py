import unittest
from language import LanguageApi


class TestLanguage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestLanguage, self).__init__(*args, **kwargs)
        self.language = LanguageApi()

    def test_detect_vision_info(self):
        res = self.language.detect_sentiment(["As University of Waterloo students, we hope to collect "
                                              "insight through sentiment analysis in memes from Reddit."])
        self.assertIsNotNone(res)
        self.assertNotEqual(res, [])


if __name__ == '__main__':
    unittest.main()
