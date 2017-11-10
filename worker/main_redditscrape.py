import requests
import reddit


class ScrapedRedditPost(object):

    def __init__(self, post, users, image_urls):
        self.post = post
        self.users = users
        self.image_urls = image_urls


def scrape_reddit(subreddit, pages=20):

    after = None

    for _ in range(pages):
        posts, after = reddit.get_new(subreddit, limit=10, after=after)
        image_url = reddit.get_previews(posts)
        users = None
        res = ScrapedRedditPost(post=posts, users=users, image_urls=image_url)
        yield res


if __name__ == '__main__':
    for scraped_info in scrape_reddit(subreddit="AdviceAnimals", pages=1):
        break

