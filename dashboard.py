import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.repositories.elasticsearch_repo import ElasticsearchRepository
from src.repositories.mysql_repo import MySQLRepository
from src.repositories.sqlite_repo import SQLiteRepository
from src.services.analysis_service import AnalysisService
from src.services.auth_service import AuthService

# Initialize Repositories and Services
es_repo = ElasticsearchRepository()
mysql_repo = MySQLRepository()
mysql_repo.setup_table() # Ensure the users table exists
sqlite_repo = SQLiteRepository()

analysis_service = AnalysisService(es_repo)
auth_service = AuthService(mysql_repo)

# --------------------
# Session State for Auth
# --------------------
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# --------------------
# Load Data Functions (Using Services/Repos)
# --------------------

@st.cache_data
def load_twitter_data():
    hits = es_repo.search_tweets()
    records = []
    for hit in hits:
        if hasattr(hit, 'timestamp') and hasattr(hit, 'sentiment_score'):
            records.append({"ds": hit.timestamp, "y": hit.sentiment_score})
    df = pd.DataFrame(records)
    if not df.empty:
        df["ds"] = pd.to_datetime(df["ds"]).dt.tz_localize(None)
    return df

@st.cache_data
def load_engagement_data(metric, location=None):
    hits = es_repo.search_tweets()
    records = []
    for hit in hits:
        if hasattr(hit, 'timestamp') and hasattr(hit, metric):
            loc = getattr(hit, "user_location", "").strip().lower()
            if location is None or loc == location:
                records.append({"ds": hit.timestamp, "y": getattr(hit, metric)})
    df = pd.DataFrame(records)
    if not df.empty:
        df["ds"] = pd.to_datetime(df["ds"]).dt.tz_localize(None)
    return df

@st.cache_data
def load_engagement_final():
    hits = es_repo.search_tweets()
    records = []
    for hit in hits:
        if hasattr(hit, 'timestamp') and hasattr(hit, 'engagement_final'):
            records.append({"ds": hit.timestamp, "y": hit.engagement_final})
    df = pd.DataFrame(records)
    if not df.empty:
        df["ds"] = pd.to_datetime(df["ds"]).dt.tz_localize(None)
    return df

@st.cache_data
def get_unique_user_locations():
    hits = es_repo.search_tweets()
    return analysis_service.get_location_counts(hits)

@st.cache_data
def get_hashtag_engagement_data():
    hits = es_repo.search_tweets()
    return analysis_service.get_hashtag_engagement(hits)

# --------------------
# Plotting Functions
# --------------------

def plot_past_data(df, title, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["ds"], df["y"], marker="o", linestyle="-")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    st.pyplot(fig)

def plot_forecast_data(df, forecast, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["ds"], df["y"], marker="o", label="Past Data")
    ax.plot(forecast["ds"], forecast["yhat"], linestyle="dashed", label="Forecast")
    ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], alpha=0.3)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Metric")
    ax.set_title(title)
    ax.legend()
    st.pyplot(fig)

# --------------------
# Streamlit App Interface
# --------------------

st.title("📊 Future Trend & Sentiment Prediction")

if st.session_state['authenticated']:
    st.sidebar.success(f"Logged in as: {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.rerun()

dataset_choice = st.sidebar.radio(
    "Select Dataset:",
    ["Google Trends", "Twitter Sentiment", "Engagement Overview", "Favourite Overview", "Register and Login", "Shared plots"]
)

if dataset_choice in ["Google Trends", "Twitter Sentiment", "Engagement Overview"]:
    forecast_seconds = st.sidebar.slider("Select number of seconds to predict:", 30, 3600, 1800, 30)

if dataset_choice == "Google Trends":
    pass

elif dataset_choice == "Twitter Sentiment":
    df = load_twitter_data()
    st.subheader("💬 Predicting Twitter Sentiment for iPhone Tweets")

    if df.empty:
        st.warning("No data available for Twitter Sentiment.")
    else:
        forecast = analysis_service.get_forecast(df, seconds=forecast_seconds)
        plot_forecast_data(df, forecast, f"Predicted Twitter Sentiment for the Next {forecast_seconds} Seconds")
        st.write(f"### Forecasted Data (Next {forecast_seconds} Seconds)")
        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(int(forecast_seconds/30)))

elif dataset_choice == "Engagement Overview":
    st.subheader("📣 Past Engagement Metrics for iPhone Tweets")

    user_locations = get_unique_user_locations()
    selected_display = st.selectbox("Filter by User Location", ["All"] + user_locations)
    selected_location = None if selected_display == "All" else selected_display.split(" (")[0].strip().lower()

    df_final = load_engagement_final()
    if df_final.empty:
        st.warning("No data available for Engagement Final.")
    else:
        plot_past_data(df_final, "Engagement Final Over Time", "Engagement Final")

        if st.button("🔍 Save Engagement Final Data to Database"):
            x_values = df_final["ds"].astype(str)
            y_values = df_final["y"]
            sqlite_repo.save_engagement(x_values, y_values)
            st.success("Data successfully saved to the database!")

        forecast = analysis_service.get_forecast(df_final, seconds=forecast_seconds)
        plot_forecast_data(df_final, forecast, f"Forecasted Engagement Final for the Next {forecast_seconds} Seconds")
        st.write(f"### Forecasted Data (Next {forecast_seconds} Seconds) for Engagement Final")
        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(int(forecast_seconds/30)))

    metrics = [
        "regular_engagement",
        "google_engagement",
        "adjusted_engagement",
        "engagement_including_sentiment",
        "high_follower_engagement"
    ]

    for metric in metrics:
        df_metric = load_engagement_data(metric, selected_location)
        if df_metric.empty:
            st.warning(f"No data available for {metric.replace('_', ' ').title()} at the selected location.")
        else:
            plot_past_data(df_metric, f"{metric.replace('_', ' ').title()} Over Time", metric.replace('_', ' ').title())
            forecast = analysis_service.get_forecast(df_metric, seconds=forecast_seconds)
            plot_forecast_data(df_metric, forecast, f"Forecasted {metric.replace('_', ' ').title()} for the Next {forecast_seconds} Seconds")
            st.write(f"### Forecasted Data (Next {forecast_seconds} Seconds) for {metric.replace('_', ' ').title()}")
            st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(int(forecast_seconds/30)))

    st.subheader("🏷️ Hashtag Engagement Table")
    df_hashtags = get_hashtag_engagement_data()
    if df_hashtags.empty:
        st.write("No hashtag data found.")
    else:
        st.dataframe(df_hashtags.reset_index(drop=True))

elif dataset_choice == "Favourite Overview":
    st.subheader("🔖 Favourites Overview")
    saved_data = sqlite_repo.get_all_engagement()

    if saved_data:
        df_saved_data = pd.DataFrame(saved_data, columns=["ID", "xAxis", "yAxis"])
        df_saved_data['xAxis'] = pd.to_datetime(df_saved_data['xAxis'], errors='coerce')
        if df_saved_data['xAxis'].isnull().any():
            st.warning("Some xAxis values could not be converted to datetime.")
        st.write("### Saved Engagement Data")
        st.dataframe(df_saved_data)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df_saved_data['xAxis'], df_saved_data['yAxis'], marker="o", linestyle="-")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Engagement Metric")
        ax.set_title("Saved Engagement Metrics Over Time")
        st.pyplot(fig)
    else:
        st.write("No data found in the database.")

elif dataset_choice == "Register and Login":
    st.subheader("🔐 Register and Login")
    tab1, tab2 = st.tabs(["Register", "Login"])

    with tab1:
        st.subheader("Create a new account")
        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm")

        if st.button("Register"):
            if password != confirm_password:
                st.error("Passwords do not match.")
            elif not username or not email or not password:
                st.error("Please fill in all fields.")
            else:
                success, message = auth_service.register(username, email, password)
                if success:
                    st.success(message)
                else:
                    st.error(message)

    with tab2:
        st.subheader("Login to your account")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            success, message = auth_service.login(login_username, login_password)
            if success:
                st.session_state['authenticated'] = True
                st.session_state['username'] = login_username
                st.success(message)
                st.rerun()
            else:
                st.error(message)
