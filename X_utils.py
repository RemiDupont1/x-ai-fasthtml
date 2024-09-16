import tweepy
from datetime import datetime
import re
import os

""" consumer_key = "NP3sdcyu8ALve0uBYamqgoUHk" # API
consumer_secret = "HQuRs41JKOKatJB2JcVuqBvawk5k3tNv3C8vYV7YujEa6pxlD1"
access_token = "1834568121606369280-D6iRDYPIZsKCXAjx2BUxlak2OXCNKT"
access_token_secret = "dR6qfuBAyiMYue3yEoafCyURGOTxHGzAlgkca8ROhKpWW"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAHl8vwEAAAAAqyxtpJscmKcLgyUdGIAxlsZgo2s%3D5p25mYmKd9OG6j5sjOFG0xSes7yXRDCr0lJe8WSnLIjkV2Z4Xf"
 """


def clean_tweet_text(text):
    # Remove emojis and special characters
    text = re.sub(r'[^\w\s@#]', '', text)
    text = text.replace( ".", "\n")
    # Remove emojis (Unicode ranges for most emojis)
    # text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', '', text)
    # Limit to 280 characters
    return text[:280]


def post_tweet(input_text, image_path=None):

    # Authenticate with Twitter
    client = tweepy.Client(
        consumer_key=os.environ.get('TWITTER_API_KEY'),
        consumer_secret=os.environ.get('TWITTER_API_SECRET'),
        access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
        bearer_token=os.environ.get('TWITTER_BEARER_TOKEN')
    )

    media_ids = None
    if image_path:
        # Créer un objet API pour télécharger l'image
        auth = tweepy.OAuthHandler(
            os.environ.get('TWITTER_API_KEY'),
            os.environ.get('TWITTER_API_SECRET')
        )
        auth.set_access_token(
            os.environ.get('TWITTER_ACCESS_TOKEN'),
            os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        )
        api = tweepy.API(auth)

        # Télécharger l'image
        media = api.media_upload(image_path)
        media_ids = [media.media_id]

    # Get current weekday, time, and seconds
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M:%S")

    tweet = clean_tweet_text(input_text)
    print(tweet)
    response = client.create_tweet(text=tweet, media_ids=media_ids)
    print(response)

    # Log the tweet
    log_file = 'logtweets.txt'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{tweet}\n")


#post_tweet("Hello de SF")

def get_last_10_tweets():
    # Authenticate with Twitter
    client = tweepy.Client(
        consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
        access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
        bearer_token=os.environ.get('TWITTER_BEARER_TOKEN')
    )
    # Get the user ID
    user = client.get_me()
    user_id = user.data.id

    # Get the user's tweets
    tweets = client.get_users_tweets(
        id=user_id,
        max_results=10,
        tweet_fields=['created_at', 'text'],
        exclude=['retweets', 'replies'],
    )

    # Format and return the tweets
    formatted_tweets = []
    if tweets.data:
        for tweet in tweets.data:
            formatted_tweets.append({
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at
            })

    return formatted_tweets

# Example usage:
# try:
#     last_tweets = get_last_10_tweets()
#     for tweet in last_tweets:
#         print(f"Tweet ID: {tweet['id']}")
#         print(f"Text: {tweet['text']}")
#         print(f"Created at: {tweet['created_at']}")
#         print("---")
# except Exception as e:
#     print(f"An error occurred: {e}")