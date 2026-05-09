import matplotlib.pyplot as plt
import pandas as pd
from src.config.settings import settings
from src.repositories.twitter_repo import TwitterRepository
from src.repositories.elasticsearch_repo import ElasticsearchRepository
from src.services.twitter_service import TwitterService

def plot_twitter_engagement(df, title):
    if df.empty:
        print("❌ Nothing to plot.")
        return

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["regular_engagement"], label="Regular Engagement")
    plt.plot(df["timestamp"], df["google_engagement"],  label="Google Engagement")
    plt.xlabel("Time")
    plt.ylabel("Engagement")
    plt.title(f"Engagement Trends – {title}")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    # Initialize repositories
    twitter_repo = TwitterRepository()
    es_repo = ElasticsearchRepository()
    
    # Initialize services
    twitter_service = TwitterService(twitter_repo)

    # Prepare ES index
    es_repo.create_index()

    # Fetch and process tweets
    print(f"🔍 Fetching and processing tweets for '{settings.PRODUCT_KEYWORD}'...")
    tweets_df = twitter_service.get_processed_tweets(settings.PRODUCT_KEYWORD, max_tweets=100)

    if not tweets_df.empty:
        # Save to Elasticsearch
        es_repo.save_tweets(tweets_df)

        # Plot engagement
        plot_twitter_engagement(tweets_df, settings.PRODUCT_KEYWORD)
    else:
        print("No tweets found.")

if __name__ == "__main__":
    main()
