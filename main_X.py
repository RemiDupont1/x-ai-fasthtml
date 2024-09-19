from LLM import generate_post, call_openai
from scroler import scroll_html_file
from X_utils import post_tweet
from google_image import telecharger_image_album


def main():
    url = "https://www.allmusic.com/newreleases"
    rendered_html = scroll_html_file(url)
    print(rendered_html)
    tweet = generate_post(rendered_html, max_length=280)
    print(tweet)
    messages = [
        {"role": "user", "content": f" there is a tweet : {tweet} give me the title of the album/song and the artist. Your answer should be in the format : title by artist, nothing else"}
    ]
    artist_and_title = call_openai(messages)
    image_path = telecharger_image_album(artist_and_title)


    post_tweet(tweet, image_path=image_path)