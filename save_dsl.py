from models import TweetDocument

def save_to_elasticsearch_dsl(df):
    if df.empty:
        print("❌ No data to save via DSL.")
        return

    for _, row in df.iterrows():
        doc = TweetDocument(**row.to_dict())
        doc.meta.id = row["tweet_id"]
        doc.save()

    print(f"✅ Saved {len(df)} tweets using DSL ORM.")
