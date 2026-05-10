import pandas as pd
from prophet import Prophet
from collections import Counter, defaultdict
import re

class AnalysisService:
    def __init__(self, es_repo):
        self.es_repo = es_repo

    def get_forecast(self, df, seconds, freq="30S"):
        if df.empty:
            return pd.DataFrame()
        
        # Calculate number of periods based on freq (30S)
        periods = int(seconds / 30)
        
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=periods, freq=freq)
        forecast = model.predict(future)
        return forecast

    def get_hashtag_engagement(self, hits):
        hashtag_engagement = defaultdict(list)
        for hit in hits:
            text = getattr(hit, "text", "")
            engagement = getattr(hit, "engagement_including_sentiment", None)
            if not text or engagement is None:
                continue
            hashtags = re.findall(r"#\w+", text)
            for tag in hashtags:
                hashtag_engagement[tag.lower()].append(engagement)
        
        table_data = [{"Hashtag": tag, "Avg Engagement": sum(vals) / len(vals)} for tag, vals in hashtag_engagement.items() if vals]
        df = pd.DataFrame(table_data).sort_values("Avg Engagement", ascending=False)
        return df

    def get_location_counts(self, hits):
        locations = [getattr(hit, "user_location", "").strip().lower() for hit in hits if hasattr(hit, "user_location")]
        location_counts = Counter(locations)
        cleaned_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
        return [f"{loc.title()} ({count})" for loc, count in cleaned_locations]
