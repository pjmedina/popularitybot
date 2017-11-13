import unittest
from vision import VisionApi


class TestVision(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestVision, self).__init__(*args, **kwargs)

    def test_detect_vision_info(self):
        vision = VisionApi()
        res = vision.detect_images_info(["https://i.redditmedia.com/sJHMQO41DlIqI6pT2HpAwkzuniaBFXBaIvqrlrx_8KA.jpg"])
        self.assertIsNotNone(res)
        self.assertNotEqual(res, [])


if __name__ == '__main__':
    unittest.main()
