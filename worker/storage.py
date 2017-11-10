import os
from pymongo import MongoClient
try:
    import configparser
except ImportError as e:
    import ConfigParser as configparser
try:
    # Python 3.x
    from urllib.parse import quote_plus
except ImportError:
    # Python 2.x
    from urllib import quote_plus


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
        print("Connecting to MongoDB with user: " + username)
        uri = "mongodb://%s:%s@%s/%s?authMechanism=SCRAM-SHA-1" \
              % (quote_plus(username), quote_plus(password), host, database_name)
        self.client = MongoClient(uri)
        self.db = self.client.get_database(database_name)

    def add_new_json(self, new_json):
        new_jsons = self.db.reddit_new_jsons
        new_json_id = new_jsons.insert_one(new_json).inserted_id

    def add_user_json(self, user_json):
        user_jsons = self.db.reddit_user_jsons
        user_json_id = user_jsons.insert_one(user_json).inserted_id

    def add_vision_to_post(self, post_id, vision_json):
        new_jsons = self.db.reddit_new_jsons
