
import sys, getopt
import reddit

from storage import Storage
from vision import VisionApi


def main(argv):
    subreddit = None
    post_count = None
    limit = None
    try:
        opts, args = getopt.getopt(argv, "hs:p:", ["subreddit=", "post_count="])
    except getopt.GetoptError:
        print('main.py -s <subreddit> -p <post_count>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -s <subreddit> -p <post_count> (optional: -l <limit>)')
            sys.exit()
        elif opt in ("-s", "--subreddit"):
            subreddit = arg
        elif opt in ("-p", "--post_count"):
            post_count = arg
        elif opt in ("-l", "--limit"):
            limit = arg
    if subreddit is None or post_count is None:
        print('main.py -s <subreddit> -p <post_count> (optional: -l <limit>)')
        sys.exit()

    vision = VisionApi()
    storage = Storage()

    # scrape reddit
    for scraped_info in reddit.scrape_reddit(subreddit="AdviceAnimals", post_count=post_count, limit=limit):
        # now pass in the image urls into the vision api
        image_info_response = vision.detect_image_info(scraped_info.image_urls)
        # for image_url, labels in zip(scraped_info.image_urls, labels_response):



# def download_image(image_url):
#     r = requests.get(image_url)
#     r.raise_for_status()
#     return r.content


def get_label_info(vision, storage, image_urls):
    # image_contents = [
    #     download_image(image_url)
    #     for image_url
    #     in image_urls]
    return


if __name__ == "__main__":
    main(sys.argv[1:])
