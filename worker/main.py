
import sys, getopt
import reddit

from storage import Storage
from vision import VisionApi


def main_args(argv):
    subreddit = None
    post_count = None
    limit = None
    try:
        opts, args = getopt.getopt(argv, "hs:p:l:", ["subreddit=", "post_count=", "limit="])
    except getopt.GetoptError:
        print('main.py -s <subreddit> -p <post_count> (optional: -l <limit>)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -s <subreddit> -p <post_count> (optional: -l <limit>)')
            sys.exit()
        elif opt in ("-s", "--subreddit"):
            subreddit = arg
        elif opt in ("-p", "--post_count"):
            post_count = int(arg)
        elif opt in ("-l", "--limit"):
            limit = int(arg)
    main(subreddit, post_count, limit)


def main(subreddit: str, post_count: int, limit: int=None):
    if subreddit is None or post_count is None:
        print('main.py -s <subreddit> -p <post_count> (optional: -l <limit>)')
        sys.exit()
    vision = VisionApi()
    storage = Storage()

    # scrape reddit
    for scraped_info in reddit.scrape_reddit(subreddit="AdviceAnimals", post_count=post_count, limit=limit):
        # now pass in the image urls into the vision api
        vision_res = vision.detect_images_info(scraped_info.image_urls)
        storage.add_reddit_scraped_info(scraped_info)
        for post, image_url, image_info in zip(scraped_info.posts, scraped_info.image_urls, vision_res['responses']):
            storage.add_vision_info(reddit.get_post_id(post), image_url=image_url, vision_json=image_info)


if __name__ == "__main__":
    main_args(sys.argv[1:])
