
import sys
import getopt
import logging
import random
from datetime import datetime
import reddit
from reddit import ScrapedRedditPost

from storage import Storage
from vision import VisionApi


def main_args(argv):
    subreddit = None
    post_count = None
    limit = None
    run_level = None
    after = None
    try:
        opts, args = getopt.getopt(argv, "hs:p:l:a:g:", ["subreddit=", "post_count=", "limit=", "after=", "loglevel="])
    except getopt.GetoptError:
        print('main.py -s <subreddit> -p <post_count> '
              '(optional: -l <limit>, -a <after>, -g <loglevel: {DEBUG (default), INFO}>)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -s <subreddit> -p <post_count> '
                  '(optional: -l <limit>, -a <after>, -g <loglevel: {DEBUG (default), INFO}>)')
            sys.exit()
        elif opt in ("-s", "--subreddit"):
            subreddit = arg
        elif opt in ("-p", "--post_count"):
            post_count = int(arg)
        elif opt in ("-l", "--limit"):
            limit = int(arg)
        elif opt in ("-g", "--loglevel"):
            run_level = arg
        elif opt in ("-a", "--after"):
            after = arg
    main(subreddit, post_count, limit, after, run_level)


def main(subreddit: str, post_count: int, limit: int=None, after: str=None, log_level: str=None):
    if subreddit is None or post_count is None:
        print('main.py -s <subreddit> -p <post_count> '
              '(optional: -l <limit>, -a <after>, -g <loglevel: {DEBUG (default), INFO}>)')
        sys.exit()

    # set up logger
    if log_level != "INFO":
        log_level = "DEBUG"
        level = logging.DEBUG
    else:
        level = "INFO"
    log_file_name = datetime.now().strftime('../logs/popularitybot_%H_%M_%d_%m_%Y_{}.log'.format(log_level))
    logging.basicConfig(filename=log_file_name, level=level, format='%(asctime)s %(message)s')

    # init vision and storage
    vision = VisionApi()
    storage = Storage()

    # scrape reddit
    for scraped_info in reddit.scrape_reddit(subreddit="AdviceAnimals", post_count=post_count, after=after, limit=limit):
        if scraped_info is None:
            logging.critical("ScrapedInfo is None. Exiting.")
            sys.exit(2)
        # clean any scraped info that has None in their posts, image_urls, or user_info
        ScrapedRedditPost.clean(scraped_info)
        if len(scraped_info.posts) < limit:
            logging.info("Removed {} posts from this scrape.".format(limit-len(scraped_info.posts)))
        rand_post_id = scraped_info.posts[random.randint(0, len(scraped_info.posts-1))]['data']['id']
        if storage.reddit_post_exists(rand_post_id):
            raise RuntimeError("Post already seen. Something is weird.")
        # now pass in the image urls into the vision api 
        vision_res = vision.detect_images_info(scraped_info.image_urls)
        storage.add_reddit_scraped_info(scraped_info)
        for post, image_url, image_info in zip(scraped_info.posts, scraped_info.image_urls, vision_res['responses']):
            storage.add_vision_info(reddit.get_post_id(post), image_url=image_url, vision_json=image_info)


if __name__ == "__main__":
    main_args(sys.argv[1:])
