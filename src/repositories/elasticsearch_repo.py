from elasticsearch_dsl import connections
from src.config.settings import settings
from src.models.tweet import TweetDocument

class ElasticsearchRepository:
    def __init__(self):
        connection_params = {
            "hosts": [settings.ES_HOST],
        }
        if settings.ES_USER and settings.ES_PASSWORD:
            connection_params["http_auth"] = (settings.ES_USER, settings.ES_PASSWORD)

        if settings.ES_USE_SSL:
            connection_params["use_ssl"] = True
            connection_params["verify_certs"] = settings.ES_VERIFY_CERTS
            if settings.ES_CA_CERTS:
                connection_params["ca_certs"] = settings.ES_CA_CERTS

        connections.create_connection(**connection_params)

    def create_index(self):
        if not TweetDocument._index.exists():
            TweetDocument.init()
            print(f"✅ DSL index '{settings.ES_INDEX}' created.")
        else:
            print(f"ℹ️ DSL index '{settings.ES_INDEX}' already exists.")

    def save_tweets(self, df):
        if df.empty:
            return
        for _, row in df.iterrows():
            doc = TweetDocument(**row.to_dict())
            doc.meta.id = row["tweet_id"]
            doc.save()
        print(f"✅ Saved {len(df)} tweets using DSL ORM.")

    def search_tweets(self, limit=10000):
        return TweetDocument.search()[:limit].execute()
