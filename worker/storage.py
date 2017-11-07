import os
from pymongo import MongoClient

class Storage(object):
    def __init__(self, host=None, port=None, *args, **kwargs):
        self.client = MongoClient()
        self.db = client.popularitybot_training

    def add_new_json(self, new_json):
        new_jsons = self.db.reddit_new_jsons
        new_json_id = new_jsons.insert_one(new_json).inserted_id

    def add_user_json(self, user_json):
        user_jsons = self.db.reddit_user_jsons
        user_json_id = user_jsons.insert_one(user_json).inserted_id

    def add_vision_to_post(self, post_id, vision_json):
        new_jsons = self.db.reddit_new_jsons
