import unittest
import json
from storage import Storage


class TestStorage(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestStorage, self).__init__(*args, **kwargs)

        # Will throw an exception if storage_creds.ini does not exist,
        # rendering all tests useless. Must have the config file available.
        self.storage = Storage(config_file='storage_creds.ini',
                               config_header='database_info',
                               new_collection_name='reddit_new_jsons',
                               user_collection_name='reddit_user_jsons',
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

    def test_for_deadline(self):
        name_link = self.storage.user_collection.find({}, {"data.name": 1, "data.link_karma": 1})
        name_score = self.storage.post_collection.find({}, {"data.author": 1, "data.score": 1})
        name_link_revised = {}
        entries = name_link[:]
        for d in entries:
            if d['data']['link_karma'] < 300000:
                name_link_revised[d['data']['name']] = {"karma": d['data']['link_karma'], "score": -1}
        entriess = name_score[:]
        for a in entriess:
            if a['data']['author'] in name_link_revised and a['data']['score'] < 10000:
                name_link_revised[a['data']['author']]['score'] = a['data']['score']
        with open('abc.json', "w") as file_name:
            json.dump(name_link_revised, file_name)


if __name__ == '__main__':
    unittest.main()
