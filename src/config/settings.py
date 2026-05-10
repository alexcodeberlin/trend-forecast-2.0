import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Twitter
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
    PRODUCT_KEYWORD = "iPhone"

    # MySQL
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "user_plot_app")
    MYSQL_SSL_CA = os.getenv("MYSQL_SSL_CA")
    MYSQL_SSL_CERT = os.getenv("MYSQL_SSL_CERT")
    MYSQL_SSL_KEY = os.getenv("MYSQL_SSL_KEY")

    # Elasticsearch
    ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
    ES_INDEX = "twitter_datav7"
    ES_USER = os.getenv("ES_USER")
    ES_PASSWORD = os.getenv("ES_PASSWORD")
    ES_USE_SSL = os.getenv("ES_USE_SSL", "False").lower() == "true"
    ES_VERIFY_CERTS = os.getenv("ES_VERIFY_CERTS", "False").lower() == "true"
    ES_CA_CERTS = os.getenv("ES_CA_CERTS")
    
    # Phase 2: mTLS for Elasticsearch (Ensure these lines exist!)
    ES_CLIENT_CERT = os.getenv("ES_CLIENT_CERT")
    ES_CLIENT_KEY = os.getenv("ES_CLIENT_KEY")

    # SQLite
    SQLITE_DB_FILE = os.getenv("SQLITE_DB_FILE", "engagement_data.db")

settings = Settings()