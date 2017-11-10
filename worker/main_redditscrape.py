import requests
import reddit

class RedditScraper:
    def scrape_reddit(self, subreddit, pages=10):
        print("YOU")
        after = None

        for _ in range(pages):
            posts, after = reddit.get_hot(subreddit, limit=10, after=after)
            print(posts)
            yield reddit.get_previews(posts)


    def scrape_reddit_task(subreddit, pages=20):
        for image_urls in scrape_reddit(subreddit, pages):
            break


if __name__ == '__main__':
    r = RedditScraper()
    r.scrape_reddit("AdviceAnimals", pages=1)
