from elasticsearch_dsl import Document, Date, Text, Keyword, Integer, Float, connections
from src.config.settings import settings

class TweetDocument(Document):
    tweet_id = Keyword()
    timestamp = Date()
    text = Text()
    sentiment_score = Float()
    likes = Integer()
    retweets = Integer()
    replies = Integer()
    clicks = Integer()
    user_location = Text(fields={"keyword": Keyword()})
    followers = Integer()
    regular_engagement = Integer()
    google_engagement = Float()
    high_follower_engagement = Float()
    adjusted_engagement = Float()
    engagement_including_sentiment = Float()
    engagement_final = Float()

    class Index:
        name = settings.ES_INDEX
        settings = {
            "number_of_shards": 3,
            "number_of_replicas": 2
        }
