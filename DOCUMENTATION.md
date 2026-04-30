# Project Documentation: Future Trend & Sentiment Analysis Platform

This documentation outlines the architecture, design, and functionality of the Trend Prediction platform. The project has been refactored into a professional Object-Oriented structure using the **Repository-Service Pattern**.

## 1. Project Overview
The application is a data analysis platform designed to fetch real-time data from the Twitter API, process it to extract sentiment and engagement metrics, and provide visual forecasts of future trends. It features a data ingestion pipeline and an interactive dashboard for end-users.

## 2. System Architecture
The project follows a layered architecture to ensure separation of concerns and maintainability:

*   **Presentation Layer (`dashboard.py`)**: A Streamlit-based web interface for data visualization, forecasting, and user interaction.
*   **Ingestion Layer (`main.py`)**: A command-line script that orchestrates the fetching, processing, and storing of new data.
*   **Business Logic Layer (`src/services/`)**: Contains the core "intelligence" of the app, such as NLP cleaning, engagement math, and time-series forecasting.
*   **Data Access Layer (`src/repositories/`)**: Handles all communication with external databases and APIs.
*   **Configuration Layer (`src/config/`)**: Centralizes application settings and environment variables.

---

## 3. Directory Structure
```text
├── src/
│   ├── config/          # Settings and environment loading
│   ├── models/          # Data structure definitions (e.g., Elasticsearch Document)
│   ├── repositories/    # Data Access Objects (Twitter, ES, MySQL, SQLite)
│   └── services/        # Business logic (Cleaning, Analysis, Auth)
├── dashboard.py         # Streamlit UI entry point
├── main.py              # Data ingestion entry point
├── requirements.txt     # Project dependencies
└── .env.example         # Template for configuration
```

---

## 4. Key Modules and Components

### 4.1 Authentication and User Management (Auth Service)
The `AuthService` handles all security-critical user operations:
*   **Registration**: Validates input, hashes passwords using Argon2id, and persists user data.
*   **Login**: Verifies credentials against the MySQL database and manages session states.
*   **Audit Integration**: Automatically logs all authentication attempts to the centralized audit repository.

### 4.2 Data Processing (Twitter Service)
The `TwitterService` is responsible for the transformation of raw API data into actionable insights:
*   **Cleaning**: Uses NLTK and Regex to remove URLs, handle emojis, strip stopwords, and perform lemmatization.
*   **Sentiment Analysis**: Utilizes `TextBlob` to assign a polarity score to each tweet.
*   **Engagement Calculation**: A custom algorithm that calculates "Final Engagement" based on likes, retweets, replies, clicks, and follower influence.

### 4.2 Analytics and Forecasting (Analysis Service)
This service handles complex data operations for the UI:
*   **Time-Series Forecasting**: Uses the **Facebook Prophet** library to predict future sentiment and engagement trends based on historical data.
*   **Hashtag Analysis**: Aggregates engagement metrics across different hashtags to identify high-performing topics.
*   **Location Tracking**: Processes and counts user locations for demographic filtering.

### 4.3 Data Management (Repositories)
*   **Twitter Repository**: Interfaces with the Tweepy library to search for recent tweets.
*   **Elasticsearch Repository**: Manages high-speed document storage and search for processed tweets.
*   **MySQL Repository**: Handles persistent user account data.
*   **SQLite Repository**: Manages a local database for "favorite" or "saved" engagement snapshots.

---

## 5. Application Workflow

### 5.1 Ingestion Pipeline (`main.py`)
1.  **Initialize**: Sets up the connection to Elasticsearch and prepares the index.
2.  **Fetch**: Retrieves the latest tweets for a specific product keyword (e.g., "iPhone").
3.  **Process**: Cleans the text and calculates engagement metrics.
4.  **Store**: Saves the enriched data into Elasticsearch for later analysis.
5.  **Visualize**: Generates a quick matplotlib plot showing immediate engagement trends.

### 5.2 Interactive Dashboard (`dashboard.py`)
The dashboard provides several views for the user:
*   **Twitter Sentiment**: Displays historical sentiment and a forecasted trend line for the next hour.
*   **Engagement Overview**: Allows filtering of metrics by user location and displays a table of top hashtags.
*   **Favorites**: Shows data points that the user has specifically saved to the local SQLite database.
*   **User Management**: Provides a tabbed interface for new user registration.

---

## 6. Setup and Installation

1.  **Dependencies**: Install required packages via pip:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configuration**: 
    - Copy `.env.example` to `.env`.
    - Fill in your API keys and database connection strings.
3.  **Run Ingestion**:
    ```bash
    python main.py
    ```
4.  **Run Dashboard**:
    ```bash
    streamlit run dashboard.py
    ```

---

## 7. Technical Stack
*   **Language**: Python 3.x
*   **Frontend**: Streamlit
*   **NLP**: TextBlob, NLTK, Emoji
*   **Databases**: Elasticsearch (NoSQL), MySQL (Relational), SQLite (Local)
*   **APIs**: Tweepy (Twitter API v2)
*   **Forecasting**: Facebook Prophet
