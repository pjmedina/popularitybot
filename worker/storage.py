import os
from pymongo import MongoClient
from reddit import ScrapedRedditPost
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

    def __init__(self,
                 config_file=None, config_header=None,
                 user_collection_name="reddit_user_jsons",
                 new_collection_name="reddit_new_jsons",
                 vision_collection_name="reddit_vision_info",
                 *args, **kwargs):
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
        self.user_collection = self.db[user_collection_name]
        self.post_collection = self.db[new_collection_name]
        self.vision_collection = self.db[vision_collection_name]

    def add_reddit_scraped_info(self, scraped_info: ScrapedRedditPost):
        for user_info in scraped_info.user_info:
            self.add_reddit_user_json(user_info)
        self.post_collection.insert_many(scraped_info.posts)

    def add_reddit_user_json(self, user_json):
        if not self.reddit_user_exists(self.get_reddit_username(user_json)):
            return self.user_collection.insert_one(user_json).inserted_id
        return None

    def add_vision_info(self, post_id, image_url, vision_json):
        if 'reddit_id' not in vision_json:
            vision_json['reddit_id'] = post_id
        if 'image_url' not in vision_json:
            vision_json['image_url'] = image_url
        return self.vision_collection.insert_one(vision_json).inserted_id

    def reddit_user_exists(self, username):
        return self.user_collection.find({"data.name": username}) != []

    def get_reddit_username(self, user_json):
        return user_json['data']['name']
