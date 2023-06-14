import feedparser
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import pandas as pd

# Set up the VADER Sentiment Analyzer
nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

# Specify the stock variable and date range
stock = "IBM"
#start_date = datetime(2020, 5, 1)
#end_date = datetime(2020, 5, 5)
start_date = datetime(2010, 1, 2)
end_date = datetime(2023, 4, 22)

# Initialize empty DataFrame to store sentiment scores
df = pd.DataFrame(columns=["Date", "Sentiment"])

day = 0
# Loop through each day in the date range
while start_date <= end_date:
    if day % 100 == 0:
        print(day)

    # Format the date for the Google News RSS URL
    date_str = start_date.strftime("%Y-%m-%d")

    # Build the Google News RSS URL for the specified stock and date
    rss_url = f"https://news.google.com/rss/search?q={stock}+when:{date_str}&hl=en-US&gl=US&ceid=US:en"

    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Calculate the average sentiment score for the news articles
    total_sentiment = 0
    num_articles = 0
    for entry in feed.entries:
        title = entry.title
        content = entry.summary

        # Check if the article mentions the stock name
        if stock.lower() in title.lower() or stock.lower() in content.lower():
            sentiment = analyzer.polarity_scores(title)
            total_sentiment += sentiment["compound"]
            num_articles += 1

    if num_articles > 0:
        avg_sentiment = total_sentiment / num_articles
    else:
        avg_sentiment = 0

    # Add the date and sentiment score to the DataFrame
    df = df.append({"Date": start_date.date(), "Sentiment": avg_sentiment}, ignore_index=True)

    # Move to the next day
    start_date += timedelta(days=1)
    day = day + 1

# Save the DataFrame to a CSV file
df.to_csv("sentiment_scores.csv", index=False)

# Print the results
#print(df)
print("done")
