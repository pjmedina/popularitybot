import unittest
import reddit
from vision import VisionApi


class TestVision(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestVision, self).__init__(*args, **kwargs)
        self.vision = VisionApi()

    def test_detect_vision_info(self):
        res = self.vision.detect_images_info(["https://i.redd.it/zr11w62i4mxz.png"])
        self.assertIsNotNone(res)
        self.assertNotEqual(res, [])


if __name__ == '__main__':
    unittest.main()
