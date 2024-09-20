import tweepy
from datetime import datetime
import re
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    text = Column(String(280))

# Database setup
DATABASE_URL = os.environ.get("POSTGRES_URL")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)



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

    # Save the tweet to the database
    session = Session()
    
    # Générer manuellement le prochain ID
    max_id = session.query(func.max(Tweet.id)).scalar()
    next_id = 1 if max_id is None else max_id + 1
    
    new_tweet = Tweet(id=next_id, text=tweet)
    session.add(new_tweet)
    session.commit()
    session.close()

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

