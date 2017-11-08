import os
from pymongo import MongoClient
try:
    import configparser
except ImportError as e:
    import ConfigParser as configparser


class Storage(object):

    def __init__(self, config_file=None, config_header=None, *args, **kwargs):
        if config_file is None:
            config_file = 'storage_creds.ini'
        if config_header is None:
            config_header = 'database_info'
        config = configparser.RawConfigParser()
        config.read(config_file)
        username = config.get(config_header, 'username')
        database_name = config.get(config_header, 'database')
        password = config.get(config_header, 'password')
        host = config.get(config_header, 'host')
        self.client = MongoClient(host,
                                  user=username,
                                  password=password,
                                  authSource=database_name,
                                  authMechanism='SCRAM-SHA-1')
        self.db = self.client.get_database()

    def add_new_json(self, new_json):
        new_jsons = self.db.reddit_new_jsons
        new_json_id = new_jsons.insert_one(new_json).inserted_id

    def add_user_json(self, user_json):
        user_jsons = self.db.reddit_user_jsons
        user_json_id = user_jsons.insert_one(user_json).inserted_id

    def add_vision_to_post(self, post_id, vision_json):
        new_jsons = self.db.reddit_new_jsons
