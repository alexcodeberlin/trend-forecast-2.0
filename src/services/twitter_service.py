import re
import pandas as pd
from textblob import TextBlob
import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Ensure NLTK resources are available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class TwitterService:
    def __init__(self, twitter_repo):
        self.twitter_repo = twitter_repo
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def get_processed_tweets(self, product, max_tweets=100):
        df = self.twitter_repo.fetch_tweets(product, max_tweets)
        if df.empty:
            return df

        df = self.clean_data(df)
        df = self.add_engagement_metrics(df)
        return df

    def clean_data(self, df):
        df = df.drop_duplicates(subset=["tweet_id"], keep="first")
        df = df.fillna({
            "text": "",
            "user_location": "Unknown",
            "followers": 0,
            "likes": 0,
            "retweets": 0,
            "replies": 0,
            "clicks": 0
        })

        def clean_text(text):
            text = emoji.demojize(text)
            text = re.sub(r"http\S+", "", text)
            text = re.sub(r"@\w+", "", text)
            text = re.sub(r"[^\w\s#]", " ", text)
            text = text.lower()
            tokens = text.split()
            tokens = [t for t in tokens if t not in self.stop_words]
            tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
            return " ".join(tokens).strip()

        df["clean_text"] = df["text"].apply(clean_text)
        df["sentiment_score"] = df["clean_text"].apply(lambda x: TextBlob(x).sentiment.polarity)
        return df

    def add_engagement_metrics(self, df, amp=1.5):
        df["regular_engagement"] = df[["likes", "retweets", "replies", "clicks"]].sum(axis=1)
        df["google_engagement"] = 0.0
        df["high_follower_engagement"] = df["regular_engagement"] * (df["followers"] >= 10000) * amp
        df["adjusted_engagement"] = df["regular_engagement"] + df["high_follower_engagement"]
        df["engagement_including_sentiment"] = df["adjusted_engagement"] * (1 + df["sentiment_score"])
        df["engagement_final"] = (
            df["regular_engagement"] +
            df["google_engagement"] +
            df["high_follower_engagement"] +
            df["adjusted_engagement"] +
            df["engagement_including_sentiment"]
        )
        return df
