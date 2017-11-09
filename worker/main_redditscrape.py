import requests
import reddit


def scrape_reddit(subreddit, pages=10):
    after = None

    for _ in range(pages):
        posts, after = reddit.get_hot(subreddit, limit=100, after=after)
        yield reddit.get_previews(posts)


def scrape_reddit_task(subreddit, pages=20):
    for image_urls in scrape_reddit(subreddit, pages):
        break


if __name__ == '__main__':
    scrape_reddit("AdviceAnimals", 1)
