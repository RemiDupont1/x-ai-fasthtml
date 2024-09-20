import requests
from LLM import generate_post, call_openai
from X_utils import post_tweet
from google_image import telecharger_image_album

def download_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def main():
    url = "https://www.allmusic.com/newreleases"
    file_content = download_html(url)
    print("file_content ok")
    tweet = generate_post(file_content, max_length=280)
    print("tweet", tweet)
    messages = [
        {"role": "user", "content": f"there is a tweet : {tweet} give me the title of the album/song and the artist. Your answer should be in the format : title by artist, nothing else"}
    ]
    artist_and_title = call_openai(messages)
    image_path = telecharger_image_album(artist_and_title)
    post_tweet(tweet, image_path=image_path)