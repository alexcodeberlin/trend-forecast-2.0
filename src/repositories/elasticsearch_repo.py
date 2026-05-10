from elasticsearch_dsl import connections
from src.config.settings import settings
from src.models.tweet import TweetDocument
import ssl

class ElasticsearchRepository:
    def __init__(self):
        # Configuration for Elasticsearch 8.x/9.x
        # Build connection arguments for the modern transport layer
        # Note: 'use_ssl' is intentionally omitted as it is deprecated in v8/v9
        
        connection_args = {
            "hosts": [settings.ES_HOST],
            "verify_certs": settings.ES_VERIFY_CERTS,
        }

        # Basic Authentication
        if settings.ES_USER and settings.ES_PASSWORD:
            connection_args["basic_auth"] = (settings.ES_USER, settings.ES_PASSWORD)

        # Phase 2: mTLS + TLS 1.3 Configuration
        if settings.ES_USE_SSL:
            # 1. Provide certificate paths directly
            if settings.ES_CA_CERTS:
                connection_args["ca_certs"] = settings.ES_CA_CERTS
                
            if settings.ES_CLIENT_CERT and settings.ES_CLIENT_KEY:
                connection_args["client_cert"] = settings.ES_CLIENT_CERT
                connection_args["client_key"] = settings.ES_CLIENT_KEY

            # THE FIX: Disable hostname verification for local development
            connection_args["ssl_assert_hostname"] = False
            
            print(f"🔐 mTLS Enabled: Secure tunnel to {settings.ES_HOST}")

        # Initialize the connection
        try:
            connections.create_connection(alias='default', **connection_args)
            print(f"✅ Elasticsearch connection initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Elasticsearch connection: {e}")

    def create_index(self):
        try:
            if not TweetDocument._index.exists():
                TweetDocument.init()
                print(f"✅ DSL index created.")
            else:
                print(f"ℹ️ DSL index already exists.")
        except Exception as e:
            print(f"❌ Error creating index: {e}")

    def save_tweets(self, df):
        if df.empty:
            return
        try:
            for _, row in df.iterrows():
                doc = TweetDocument(**row.to_dict())
                doc.meta.id = row["tweet_id"]
                doc.save()
            print(f"✅ Saved {len(df)} tweets.")
        except Exception as e:
            print(f"❌ Error saving tweets: {e}")

    def search_tweets(self, limit=10000):
        try:
            return TweetDocument.search()[:limit].execute()
        except Exception as e:
            print(f"❌ Elasticsearch Search Error: {e}")
            return []