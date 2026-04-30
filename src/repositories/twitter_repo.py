import time
import tweepy
import pandas as pd
from src.config.settings import settings

class TwitterRepository:
    def __init__(self):
        self.client = tweepy.Client(bearer_token=settings.TWITTER_BEARER_TOKEN)

    def fetch_tweets(self, product, max_tweets=10):
        try:
            resp = self.client.search_recent_tweets(
                query=f"{product} lang:en -is:retweet",
                max_results=max_tweets,
                tweet_fields=["created_at", "public_metrics", "author_id"],
                user_fields=["location", "public_metrics"],
                expansions=["author_id"]
            )
        except tweepy.errors.TooManyRequests as e:
            reset = int(e.response.headers.get("x-rate-limit-reset", time.time()))
            wait = reset - int(time.time()) + 1
            print(f"⏱ Rate limit, waiting {wait}s…")
            time.sleep(wait)
            return self.fetch_tweets(product, max_tweets)

        if not resp or not resp.data:
            return pd.DataFrame()

        users = {
            u.id: {
                "location": u.location or "Unknown",
                "followers": u.public_metrics["followers_count"]
            }
            for u in resp.includes.get("users", [])
        }

        rows = []
        for t in resp.data:
            u = users.get(t.author_id, {"location": "Unknown", "followers": 0})
            rows.append({
                "tweet_id": str(t.id),
                "timestamp": t.created_at,
                "text": t.text,
                "likes": t.public_metrics.get("like_count", 0),
                "retweets": t.public_metrics.get("retweet_count", 0),
                "replies": t.public_metrics.get("reply_count", 0),
                "clicks": int(t.public_metrics.get("like_count", 0) * 0.1),
                "user_location": u["location"],
                "followers": u["followers"]
            })

        return pd.DataFrame(rows)
